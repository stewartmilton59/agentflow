from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Category, Product, StockMovement
from sales.models import Sale, SaleItem


class InventoryStockMovementTests(TestCase):
    def test_stock_movement_page_renders_when_created_by_is_missing(self):
        user = get_user_model().objects.create_user(username='tester', email='tester@example.com', password='secret123')
        product = Product.objects.create(
            name='Test Product',
            sku='TEST-001',
            purchase_price=10,
            selling_price=15,
            current_stock=10,
            category=Category.objects.create(name='Test Category', slug='test-category'),
        )
        StockMovement.objects.create(
            product=product,
            movement_type='purchase',
            quantity=10,
            previous_quantity=0,
            new_quantity=10,
            created_by=None,
        )

        self.client.force_login(user)
        response = self.client.get(reverse('inventory:stock_movement'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'System')

    def test_product_creation_persists_batch_expiry_and_pack_size(self):
        user = get_user_model().objects.create_user(username='product-user', email='product@example.com', password='secret123')
        category = Category.objects.create(name='Test Category', slug='test-category')

        self.client.force_login(user)
        response = self.client.post(reverse('inventory:product_create'), {
            'name': 'Test Medicine',
            'generic_name': 'Generic Test',
            'purchase_price': '1000',
            'selling_price': '1300',
            'markup_percentage': '30',
            'batch_number': 'BATCH-001',
            'expiry_date': '2030-12-31',
            'pack_size': '10 tablets',
        })

        self.assertEqual(response.status_code, 302)
        product = Product.objects.get(name='Test Medicine')
        self.assertEqual(product.batch_number, 'BATCH-001')
        self.assertEqual(product.expiry_date, date(2030, 12, 31))
        self.assertEqual(product.pack_size, '10 tablets')
