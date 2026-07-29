import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.db.models import F

class Company(models.Model):
    """Company/Business Information"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    legal_name = models.CharField(max_length=200, blank=True)
    tax_id = models.CharField(max_length=50, blank=True, verbose_name="Tax ID/TIN")
    registration_no = models.CharField(max_length=100, blank=True)

    # Contact Information
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    mobile = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)

    # Address
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, default='Tanzania')

    # P.O.BOX
    p_o_box = models.CharField(max_length=100, blank=True, verbose_name="P.O.BOX")

    # Location
    location = models.CharField(max_length=200, blank=True, help_text="e.g. Kariakoo, Dar es salaam, Tanzania")

    # Branding
    logo = models.ImageField(upload_to='company/', blank=True, null=True)
    favicon = models.ImageField(upload_to='company/', blank=True, null=True)

    # Theme Color
    primary_color = models.CharField(max_length=7, default='#0d5c3a', help_text="Primary color for the system and all receipts")
    color_changes_remaining = models.IntegerField(default=5, help_text="Number of color changes remaining (max 5)")

    # Settings
    currency = models.CharField(max_length=3, default='TZS')
    currency_symbol = models.CharField(max_length=5, default='TSh')
    date_format = models.CharField(max_length=20, default='Y-m-d')
    time_format = models.CharField(max_length=20, default='H:i')
    timezone = models.CharField(max_length=50, default='Africa/Dar_es_Salaam')

    # Features
    enable_loyalty = models.BooleanField(default=True)
    enable_prescription = models.BooleanField(default=True)
    enable_multi_branch = models.BooleanField(default=False)
    enable_email_notifications = models.BooleanField(default=True)
    enable_sms_notifications = models.BooleanField(default=False)

    # Invoice Settings
    invoice_prefix = models.CharField(max_length=20, default='INV')
    invoice_footer_text = models.TextField(blank=True, help_text="Text to appear on all invoices")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Company Information"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Ensure only one company record exists
        if not self.pk and Company.objects.exists():
            raise Exception("Only one company record is allowed")
        super().save(*args, **kwargs)

class PaymentMethod(models.Model):
    """Bank/Payment accounts for invoices"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='payment_methods')
    bank_name = models.CharField(max_length=200, help_text="e.g. NMB Bank, CRDB Bank")
    account_name = models.CharField(max_length=200, help_text="Account holder name")
    account_number = models.CharField(max_length=100, help_text="Bank account number")
    is_active = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sort_order', 'bank_name']

    def __str__(self):
        return f"{self.bank_name} - {self.account_number}"


class Branch(models.Model):
    """Branch/Store Information (for multi-branch setup)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_branches')
    is_main_branch = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class SystemSetting(models.Model):
    """System-wide settings"""
    SETTING_TYPES = (
        ('general', 'General'),
        ('notification', 'Notification'),
        ('printer', 'Printer'),
        ('backup', 'Backup'),
        ('security', 'Security'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    setting_key = models.CharField(max_length=100, unique=True)
    setting_value = models.TextField()
    setting_type = models.CharField(max_length=20, choices=SETTING_TYPES, default='general')
    description = models.TextField(blank=True)
    is_encrypted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['setting_type', 'setting_key']

    def __str__(self):
        return f"{self.setting_key}: {self.setting_value[:50]}"

class Notification(models.Model):
    """System notifications"""
    NOTIFICATION_TYPES = (
        ('info', 'Information'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('alert', 'Alert'),
    )

    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='info')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    link = models.CharField(max_length=500, blank=True, help_text="URL to redirect when clicked")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.email}"

    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()

class EmailTemplate(models.Model):
    """Email templates for system emails"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    subject = models.CharField(max_length=200)
    body = models.TextField()
    variables = models.JSONField(default=list, help_text="List of available variables")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def render_body(self, context):
        """Render template with context variables"""
        body = self.body
        for key, value in context.items():
            body = body.replace(f"{{{{{key}}}}}", str(value))
        return body

class Document(models.Model):
    """Document management for receipts, invoices, etc."""
    DOCUMENT_TYPES = (
        ('invoice', 'Invoice'),
        ('receipt', 'Receipt'),
        ('prescription', 'Prescription'),
        ('purchase_order', 'Purchase Order'),
        ('report', 'Report'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    document_number = models.CharField(max_length=100)
    file = models.FileField(upload_to='documents/%Y/%m/')
    related_model = models.CharField(max_length=100, blank=True)
    related_id = models.CharField(max_length=100, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    size = models.IntegerField(default=0, help_text="File size in bytes")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_document_type_display()} - {self.document_number}"

class ActivityLog(models.Model):
    """System-wide activity logging"""
    ACTION_CHOICES = (
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('view', 'View'),
        ('export', 'Export'),
        ('import', 'Import'),
        ('print', 'Print'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('error', 'Error'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100, blank=True)
    object_id = models.CharField(max_length=100, blank=True)
    object_repr = models.CharField(max_length=200, blank=True)
    changes = models.JSONField(default=dict, blank=True, help_text="JSON of changes made")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    url = models.CharField(max_length=500, blank=True)
    method = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Activity Logs"

    def __str__(self):
        user = self.user.email if self.user else "Anonymous"
        return f"{user} - {self.action} - {self.created_at}"

class Backup(models.Model):
    """System backup records"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    backup_type = models.CharField(max_length=20, choices=[('database', 'Database'), ('media', 'Media Files'), ('full', 'Full System')])
    file_path = models.CharField(max_length=500)
    file_size = models.BigIntegerField(default=0, help_text="Size in bytes")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    error_message = models.TextField(blank=True)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"