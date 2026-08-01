import uuid
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class ExpenseCategory(models.Model):
    """Expense categories - e.g. electricity bills, rent, salaries"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="FontAwesome icon class")
    color = models.CharField(max_length=7, default='#0d5c3a', help_text="Color used in charts")
    is_frequent = models.BooleanField(
        default=False,
        help_text="Mark frequently recurring expenses (e.g. electricity, rent) for quick selection",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Expense Categories"
        ordering = ['-is_frequent', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Expense(models.Model):
    """Business expense record"""

    PAYMENT_METHODS = (
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('mobile_money', 'Mobile Money'),
        ('bank_transfer', 'Bank Transfer'),
        ('credit', 'Credit'),
        ('cheque', 'Cheque'),
        ('other', 'Other'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    expense_number = models.CharField(max_length=50, unique=True, blank=True)
    category = models.ForeignKey(
        ExpenseCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='expenses',
        help_text="Select a category for frequent/recurring expenses. Leave empty for one-off expenses.",
    )
    description = models.CharField(max_length=300, blank=True, help_text="Short description of the expense")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    expense_date = models.DateField(default=timezone.now)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash')
    paid_to = models.CharField(max_length=200, blank=True, help_text="Vendor / supplier / recipient name")
    reference_number = models.CharField(max_length=100, blank=True, help_text="Receipt / invoice number")
    notes = models.TextField(blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='expenses_created',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-expense_date', '-created_at']
        indexes = [
            models.Index(fields=['expense_date']),
            models.Index(fields=['category']),
            models.Index(fields=['payment_method']),
        ]

    def __str__(self):
        return f"{self.category.name if self.category else 'Uncategorized'} - TSh {self.amount}"

    def save(self, *args, **kwargs):
        if not self.expense_number:
            date_str = timezone.now().strftime('%Y%m%d')
            unique_str = str(uuid.uuid4())[:6].upper()
            self.expense_number = f"EXP{date_str}{unique_str}"
        super().save(*args, **kwargs)

    @property
    def amount_rounded(self):
        return Decimal(self.amount).quantize(Decimal('0.01'))
