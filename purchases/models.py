import uuid
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal


class PurchaseOrder(models.Model):
    """Purchase Order for ordering products - Simplified"""
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    po_number = models.CharField(max_length=50, unique=True, blank=True)
    invoice_number = models.CharField(max_length=100, blank=True, null=True)
    supplier_name = models.CharField(max_length=200, blank=True)

    # Order Details
    order_date = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True)

    # Financial
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    # Tracking
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='pos_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['po_number']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.po_number}"

    def save(self, *args, **kwargs):
        if not self.po_number:
            year = timezone.now().strftime('%Y')
            month = timezone.now().strftime('%m')
            prefix = f"PO{year}{month}"
            last_po = PurchaseOrder.objects.filter(
                po_number__startswith=prefix
            ).order_by('-po_number').first()

            if last_po:
                last_number = int(last_po.po_number[-4:])
                new_number = last_number + 1
            else:
                new_number = 1

            self.po_number = f"{prefix}{str(new_number).zfill(4)}"

        super().save(*args, **kwargs)

    def calculate_totals(self):
        """Calculate order totals"""
        items = self.items.all()
        self.subtotal = sum(item.subtotal for item in items)
        self.total_amount = self.subtotal
        self.save(update_fields=['subtotal', 'total_amount'])


class PurchaseOrderItem(models.Model):
    """Items in purchase order"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('inventory.Product', on_delete=models.CASCADE, related_name='purchase_items')

    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    markup_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    selling_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    batch_number = models.CharField(max_length=100, blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.purchase_order.po_number} - {self.product.name}"

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.unit_price

        if self.selling_price is None and self.markup_percent:
            self.selling_price = self.unit_price * (Decimal('1') + (self.markup_percent / Decimal('100')))

        if self.selling_price is None:
            self.selling_price = self.product.selling_price or self.unit_price

        super().save(*args, **kwargs)