from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from inventory.models import Category, Product, StockAlert
from purchases.models import PurchaseOrder


class PurchaseOrderBatchWorkflowTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='StrongPass123',
            role='admin'
        )
        self.client.force_login(self.user)

        self.category = Category.objects.create(name='Antibiotics', slug='antibiotics')
        self.product = Product.objects.create(
            name='Amoxycillin 500mg',
            sku='AMX-001',
            category=self.category,
            purchase_price=Decimal('14.00'),
            selling_price=Decimal('20.00'),
            current_stock=0,
            reorder_level=5,
            batch_number='OLD-BATCH',
            expiry_date=date(2026, 1, 10),
            created_by=self.user,
        )

    def test_purchase_order_can_store_invoice_supplier_batch_and_selling_details(self):
        response = self.client.post(
            reverse('purchases:purchase_order_create'),
            data={
                'notes': 'Receive supplier stock',
                'invoice_number': 'INV-1001',
                'supplier_name': 'Acme Pharmacy Supplies',
                'items-TOTAL_FORMS': '1',
                'items-INITIAL_FORMS': '0',
                'items-MIN_NUM_FORMS': '0',
                'items-MAX_NUM_FORMS': '1000',
                'items-0-product': str(self.product.id),
                'items-0-quantity': '5',
                'items-0-unit_price': '15.00',
                'items-0-batch_number': 'NEW-BATCH-001',
                'items-0-expiry_date': '2027-12-31',
                'items-0-markup_percent': '30',
                'items-0-selling_price': '19.50',
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)

        order = PurchaseOrder.objects.get(invoice_number='INV-1001')
        self.assertEqual(order.supplier_name, 'Acme Pharmacy Supplies')
        self.assertEqual(order.items.count(), 1)

        item = order.items.get()
        self.assertEqual(item.batch_number, 'NEW-BATCH-001')
        self.assertEqual(str(item.expiry_date), '2027-12-31')
        self.assertEqual(str(item.markup_percent), '30.00')
        self.assertEqual(str(item.selling_price), '19.50')

        self.product.refresh_from_db()
        self.assertEqual(self.product.current_stock, 5)
        self.assertEqual(self.product.batch_number, 'NEW-BATCH-001')
        self.assertEqual(str(self.product.expiry_date), '2027-12-31')
        self.assertEqual(str(self.product.purchase_price), '15.00')
        self.assertEqual(str(self.product.selling_price), '19.50')

    def test_stock_alerts_resolve_when_stock_is_replenished(self):
        alert = StockAlert.objects.create(
            product=self.product,
            alert_type='low_stock',
            message='Low stock',
            current_value=0,
            threshold_value=5,
            status='active',
        )

        self.product.current_stock = 6
        self.product.save(update_fields=['current_stock'])

        alert.refresh_from_db()
        self.assertEqual(alert.status, 'resolved')
