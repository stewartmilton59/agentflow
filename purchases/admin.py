from django.contrib import admin
from django.utils.html import format_html
from .models import PurchaseOrder, PurchaseOrderItem


class PurchaseOrderItemInline(admin.TabularInline):
    model = PurchaseOrderItem
    extra = 1
    fields = ['product', 'quantity', 'unit_price', 'subtotal']
    readonly_fields = ['subtotal']


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['po_number', 'order_date', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'order_date', 'created_at']
    search_fields = ['po_number', 'notes']
    readonly_fields = ['po_number', 'subtotal', 'total_amount', 'created_at', 'updated_at']
    fieldsets = (
        ('Order Information', {
            'fields': ('po_number', 'order_date', 'status', 'notes')
        }),
        ('Financial', {
            'fields': ('subtotal', 'total_amount')
        }),
        ('Tracking', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )
    inlines = [PurchaseOrderItemInline]
    list_per_page = 25


@admin.register(PurchaseOrderItem)
class PurchaseOrderItemAdmin(admin.ModelAdmin):
    list_display = ['purchase_order', 'product', 'quantity', 'unit_price', 'subtotal']
    list_filter = ['purchase_order__status']
    search_fields = ['purchase_order__po_number', 'product__name']
    readonly_fields = ['subtotal']
