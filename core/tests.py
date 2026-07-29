from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from inventory.models import Category, Product
from sales.models import CreditRecord, Customer, Payment, Sale


class DashboardCreditAndSalesTests(TestCase):
    def test_dashboard_counts_credit_repayments_on_payment_day_and_lists_recent_credits(self):
        user = get_user_model().objects.create_superuser(username='dashboard-admin', email='dashboard@example.com', password='secret123')
        user.role = 'admin'
        user.save(update_fields=['role'])

        category = Category.objects.create(name='Test Category', slug='test-category')
        product = Product.objects.create(
            name='Test Product',
            sku='SKU-TEST-1',
            purchase_price=100,
            selling_price=120,
            current_stock=10,
            category=category,
        )
        customer = Customer.objects.create(
            first_name='Jane',
            last_name='Doe',
            tin='TIN-001',
            fin='FIN-001',
            phone_number='0770000001',
            address='Test Address',
            city='Dar es Salaam',
            state='DSM',
            postal_code='00000',
            created_by=user,
        )
        sale = Sale.objects.create(
            invoice_number='INVTEST001',
            customer=customer,
            customer_name='Jane Doe',
            total_amount=Decimal('1000'),
            amount_paid=Decimal('0'),
            payment_status='unpaid',
            status='completed',
            created_by=user,
            created_at=timezone.now() - timedelta(days=1),
            sale_date=timezone.now() - timedelta(days=1),
        )
        credit = CreditRecord.objects.create(
            credit_number='CREDTEST001',
            sale=sale,
            customer=customer,
            customer_name='Jane Doe',
            credit_amount=Decimal('1000'),
            amount_paid=Decimal('0'),
            remaining_balance=Decimal('1000'),
            created_by=user,
            created_at=timezone.now() - timedelta(days=1),
        )
        Payment.objects.create(
            sale=sale,
            amount=Decimal('250'),
            payment_method='cash',
            notes='Credit repayment for CREDTEST001',
            created_by=user,
            created_at=timezone.now(),
        )

        self.client.force_login(user)
        response = self.client.get(reverse('core:dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['today_sales']['total'], 250.0)
        self.assertIn(credit, response.context['recent_credits'])
