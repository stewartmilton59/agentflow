from django.contrib import admin
from django.utils.html import format_html
from .models import Customer, Sale, SaleItem, Payment, CreditRecord, LoyaltyCard, LoyaltyTransaction


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0
    fields = ['product', 'quantity', 'unit_price', 'subtotal']
    readonly_fields = ['subtotal']


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    fields = ['amount', 'payment_method', 'reference_number', 'created_at']
    readonly_fields = ['created_at']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['customer_code', 'get_full_name', 'phone_number', 'customer_type', 'loyalty_points', 'is_active']
    list_filter = ['customer_type', 'is_active']
    search_fields = ['customer_code', 'first_name', 'last_name', 'phone_number', 'email']
    readonly_fields = ['customer_code', 'loyalty_points', 'total_spent', 'created_at', 'updated_at']
    list_per_page = 25


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'get_display_customer_name', 'sale_date', 'total_amount', 'payment_status', 'status']
    list_filter = ['status', 'payment_status', 'sale_date', 'has_credit']
    search_fields = ['invoice_number', 'customer__first_name', 'customer__last_name', 'customer_name']
    readonly_fields = ['invoice_number', 'subtotal', 'tax_amount', 'total_amount', 'credit_amount', 'created_at', 'updated_at']
    inlines = [SaleItemInline, PaymentInline]
    list_per_page = 25


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_number', 'sale', 'amount', 'payment_method', 'created_at']
    list_filter = ['payment_method', 'created_at']
    search_fields = ['payment_number', 'sale__invoice_number', 'reference_number']
    readonly_fields = ['payment_number', 'created_at']
    list_per_page = 25


@admin.register(CreditRecord)
class CreditRecordAdmin(admin.ModelAdmin):
    list_display = ['credit_number', 'get_customer_display', 'credit_amount', 'remaining_balance', 'status', 'due_date']
    list_filter = ['status', 'created_at']
    search_fields = ['credit_number', 'customer__first_name', 'customer__last_name', 'customer_name']
    readonly_fields = ['credit_number', 'remaining_balance']
    list_per_page = 25


@admin.register(LoyaltyCard)
class LoyaltyCardAdmin(admin.ModelAdmin):
    list_display = ['card_number', 'customer', 'points_balance', 'is_active']
    list_filter = ['is_active']
    search_fields = ['card_number', 'customer__first_name', 'customer__last_name']


@admin.register(LoyaltyTransaction)
class LoyaltyTransactionAdmin(admin.ModelAdmin):
    list_display = ['loyalty_card', 'transaction_type', 'points', 'balance_after', 'created_at']
    list_filter = ['transaction_type', 'created_at']
    search_fields = ['loyalty_card__card_number', 'description']
    list_per_page = 25
