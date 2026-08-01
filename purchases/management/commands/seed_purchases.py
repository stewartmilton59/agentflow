from decimal import Decimal
from datetime import timedelta
import random

from django.core.management.base import BaseCommand
from django.utils import timezone

from inventory.models import Product
from purchases.models import PurchaseOrder, PurchaseOrderItem

SUPPLIERS = [
    ("Rapid Africa Pharmaceuticals Ltd", "BULK RESTOCK"),
    ("Zanif Pharma Distributors", "MONTHLY REORDER"),
    ("Medical Express (T) Ltd", "EMERGENCY RESTOCK"),
    ("Geita Medical Supplies", "QUARTERLY REORDER"),
]


class Command(BaseCommand):
    help = "Seed a few completed purchase orders so Recent Purchases displays on the finance dashboard."

    def handle(self, *args, **options):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        created_by = User.objects.filter(is_superuser=True).first()

        if PurchaseOrder.objects.exists():
            self.stdout.write(self.style.WARNING(
                f"Purchase orders already exist ({PurchaseOrder.objects.count()}) - skipping."
            ))
            return

        products = list(Product.objects.filter(is_active=True))
        if not products:
            self.stdout.write(self.style.ERROR(
                "No products found. Run 'seed_products' first."
            ))
            return

        random.seed(2026)
        today = timezone.now().replace(hour=12, minute=0, second=0, microsecond=0)

        for i in range(5):
            order_date = today - timedelta(days=4 * i)
            po = PurchaseOrder.objects.create(
                supplier_name=random.choice(SUPPLIERS)[0],
                order_date=order_date,
                notes=random.choice(SUPPLIERS)[1],
                status='completed',
                created_by=created_by,
            )

            chosen = random.sample(products, k=random.randint(3, 6))
            subtotal = Decimal('0')
            for product in chosen:
                qty = random.randint(20, 200)
                unit_price = (product.purchase_price or Decimal('0')) * Decimal('0.92')
                unit_price = unit_price.quantize(Decimal('0.01'))
                PurchaseOrderItem.objects.create(
                    purchase_order=po,
                    product=product,
                    quantity=qty,
                    unit_price=unit_price,
                    markup_percent=Decimal('30'),
                    selling_price=(unit_price * Decimal('1.30')).quantize(Decimal('0.01')),
                    subtotal=(unit_price * qty).quantize(Decimal('0.01')),
                )
                subtotal += unit_price * qty

            po.subtotal = subtotal.quantize(Decimal('0.01'))
            po.total_amount = po.subtotal
            po.save(update_fields=['subtotal', 'total_amount'])

        self.stdout.write(self.style.SUCCESS(
            f"Created {PurchaseOrder.objects.count()} completed purchase orders."
        ))
