from django.contrib import admin
from django.utils.html import format_html
from .models import Company, PaymentMethod, Branch, SystemSetting, Notification, EmailTemplate, Document, ActivityLog, Backup


class PaymentMethodInline(admin.TabularInline):
    model = PaymentMethod
    extra = 1
    fields = ['bank_name', 'account_name', 'account_number', 'is_active', 'sort_order']
    ordering = ['sort_order']


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'currency']
    fieldsets = (
        ('Basic Information', {'fields': ('name', 'legal_name', 'tax_id', 'registration_no')}),
        ('Contact', {'fields': ('email', 'phone', 'mobile', 'website')}),
        ('Address', {'fields': ('address', 'city', 'state', 'postal_code', 'country', 'p_o_box', 'location')}),
        ('Branding', {'fields': ('logo', 'favicon', 'primary_color', 'color_changes_remaining')}),
        ('Settings', {'fields': ('currency', 'currency_symbol', 'date_format', 'time_format', 'timezone', 'invoice_prefix', 'invoice_footer_text')}),
        ('Features', {'fields': ('enable_loyalty', 'enable_prescription', 'enable_multi_branch', 'enable_email_notifications', 'enable_sms_notifications')}),
    )
    inlines = [PaymentMethodInline]
    readonly_fields = ('color_changes_remaining',)


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'company', 'is_main_branch', 'is_active']
    list_filter = ['is_main_branch', 'is_active', 'company']


@admin.register(SystemSetting)
class SystemSettingAdmin(admin.ModelAdmin):
    list_display = ['setting_key', 'setting_value', 'setting_type', 'description']
    list_filter = ['setting_type']
    search_fields = ['setting_key', 'description']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['title', 'message']


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'subject']


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['document_type', 'document_number', 'created_by', 'created_at']
    list_filter = ['document_type', 'created_at']
    search_fields = ['document_number']


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'model_name', 'created_at', 'ip_address']
    list_filter = ['action', 'created_at']
    search_fields = ['user__email', 'object_repr']
    readonly_fields = ['id', 'created_at']
    list_per_page = 50

    def has_add_permission(self, request):
        return False


@admin.register(Backup)
class BackupAdmin(admin.ModelAdmin):
    list_display = ['name', 'backup_type', 'status', 'file_size', 'started_at', 'completed_at']
    list_filter = ['backup_type', 'status', 'started_at']
    readonly_fields = ['id', 'started_at', 'completed_at']
