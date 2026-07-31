import uuid
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.utils.text import slugify
from decimal import Decimal
from django.db.models import F
import os


class Category(models.Model):
    """Product categories"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="FontAwesome icon class")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    """Main product model"""
    PRODUCT_TYPES = (
        ('medicine', 'Medicine'),
        ('equipment', 'Medical Equipment'),
        ('consumable', 'Consumable'),
        ('cosmetic', 'Cosmetic'),
        ('other', 'Other'),
    )

    PRESCRIPTION_REQUIRED = (
        ('none', 'No Prescription Required'),
        ('prescription', 'Prescription Required'),
        ('controlled', 'Controlled Substance'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Basic Information
    name = models.CharField(max_length=200)
    generic_name = models.CharField(max_length=200, blank=True, help_text="Generic name for medicines")
    sku = models.CharField(max_length=50, unique=True, blank=True, help_text="Stock Keeping Unit")
    barcode = models.CharField(max_length=50, unique=True, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPES, default='medicine')
    
    # Batch & Expiry Fields
    batch_number = models.CharField(max_length=100, blank=True, null=True)
    manufacturing_date = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    
    # Pack size field
    pack_size = models.CharField(max_length=100, blank=True, help_text="Pack size description (e.g., 100 tablets, 30 capsules, 250ml bottle)")

    # Pricing
    purchase_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    selling_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    wholesale_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    discount_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    vat_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=18,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    # Inventory Settings
    reorder_level = models.IntegerField(default=2, help_text="Alert when stock falls below this level")
    reorder_quantity = models.IntegerField(default=100, help_text="Quantity to reorder")
    max_stock_level = models.IntegerField(null=True, blank=True, help_text="Maximum stock limit")

    # Stock Information
    current_stock = models.IntegerField(default=0)
    minimum_stock = models.IntegerField(default=5)
    maximum_stock = models.IntegerField(default=999999999)
    unit = models.CharField(max_length=20, default='piece', help_text="Unit of measurement (e.g., tablet, bottle, box)")

    # Regulatory
    prescription_required = models.CharField(max_length=20, choices=PRESCRIPTION_REQUIRED, default='none')
    is_controlled = models.BooleanField(default=False, help_text="Is this a controlled substance?")
    requires_license = models.BooleanField(default=False)
    license_number = models.CharField(max_length=100, blank=True)

    # Additional Information
    description = models.TextField(blank=True)
    ingredients = models.TextField(blank=True, help_text="Active ingredients")
    dosage = models.CharField(max_length=200, blank=True)
    side_effects = models.TextField(blank=True)
    storage_conditions = models.CharField(max_length=200, blank=True)

    # Images
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    # Status
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_prescription = models.BooleanField(default=False)

    # Tracking
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='products_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['barcode']),
            models.Index(fields=['name']),
            models.Index(fields=['is_active']),
            models.Index(fields=['category']),
            models.Index(fields=['expiry_date']),
        ]

    def __str__(self):
        return f"{self.name} ({self.sku})"

    def save(self, *args, **kwargs):
        if not self.sku:
            prefix = self.category.slug[:3].upper() if self.category else 'PRD'
            self.sku = f"{prefix}{str(uuid.uuid4())[:8].upper()}"

        # Auto-calculate selling price if not set (30% markup)
        if not self.selling_price and self.purchase_price:
            self.selling_price = self.purchase_price * Decimal('1.30')

        super().save(*args, **kwargs)

    @property
    def profit_margin(self):
        """Calculate profit margin percentage"""
        if self.purchase_price > 0 and self.selling_price:
            return ((self.selling_price - self.purchase_price) / self.purchase_price) * 100
        return 0

    @property
    def stock_value(self):
        """Calculate total stock value"""
        return self.current_stock * self.purchase_price

    @property
    def is_low_stock(self):
        """Check if product is low on stock"""
        return self.current_stock <= self.reorder_level

    @property
    def is_out_of_stock(self):
        """Check if product is out of stock"""
        return self.current_stock <= 0


class StockMovement(models.Model):
    """Track all stock movements"""
    MOVEMENT_TYPES = (
        ('purchase', 'Purchase'),
        ('sale', 'Sale'),
        ('return', 'Return'),
        ('adjustment', 'Adjustment'),
        ('transfer', 'Transfer'),
        ('expired', 'Expired'),
        ('damaged', 'Damaged'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='movements')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.IntegerField()
    previous_quantity = models.IntegerField(default=0)
    new_quantity = models.IntegerField(default=0)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    reference_type = models.CharField(max_length=50, blank=True, help_text="e.g., Sale, Purchase Order")
    reference_id = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['product']),
            models.Index(fields=['movement_type']),
            models.Index(fields=['reference_type', 'reference_id']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.product.name} - {self.movement_type} - {self.quantity}"


class StockAlert(models.Model):
    """Stock alerts for low stock"""
    ALERT_TYPES = (
        ('low_stock', 'Low Stock'),
        ('out_of_stock', 'Out of Stock'),
        ('expiring_soon', 'Expiring Soon'),
        ('expired', 'Expired'),
    )

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('resolved', 'Resolved'),
        ('ignored', 'Ignored'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='alerts')
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    message = models.TextField()
    current_value = models.IntegerField(help_text="Current stock")
    threshold_value = models.IntegerField(help_text="Alert threshold")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resolved_alerts'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['alert_type']),
            models.Index(fields=['product', 'alert_type', 'status']),
        ]

    def __str__(self):
        return f"{self.product.name} - {self.get_alert_type_display()}"

    def resolve(self, user):
        """Mark alert as resolved"""
        self.status = 'resolved'
        self.resolved_at = timezone.now()
        self.resolved_by = user
        self.save()


class InventoryAdjustment(models.Model):
    """Inventory adjustments for stock takes"""
    ADJUSTMENT_REASONS = (
        ('damage', 'Damaged Goods'),
        ('expiry', 'Expired Products'),
        ('theft', 'Theft/Loss'),
        ('miscount', 'Miscount'),
        ('other', 'Other'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    adjustment_number = models.CharField(max_length=50, unique=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='adjustments')
    reason = models.CharField(max_length=20, choices=ADJUSTMENT_REASONS)
    quantity = models.IntegerField()
    previous_quantity = models.IntegerField()
    new_quantity = models.IntegerField()
    notes = models.TextField(blank=True)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='approved_adjustments'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_adjustments'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.adjustment_number} - {self.product.name}"

    def save(self, *args, **kwargs):
        if not self.adjustment_number:
            date_str = timezone.now().strftime('%Y%m%d')
            unique_str = str(uuid.uuid4())[:6].upper()
            self.adjustment_number = f"ADJ{date_str}{unique_str}"
        super().save(*args, **kwargs)