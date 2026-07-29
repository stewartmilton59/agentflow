from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, StockMovement, StockAlert, InventoryAdjustment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'is_active']
    list_filter = ['is_active', 'parent']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'category', 'current_stock', 'selling_price', 'product_type', 'is_active']
    list_filter = ['category', 'product_type', 'is_active', 'prescription_required']
    search_fields = ['name', 'generic_name', 'sku', 'barcode']
    readonly_fields = ['sku', 'created_at', 'updated_at']
    list_per_page = 25

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'generic_name', 'sku', 'barcode', 'category', 'product_type', 'pack_size')
        }),
        ('Batch & Dates', {
            'fields': ('batch_number', 'manufacturing_date', 'expiry_date')
        }),
        ('Pricing', {
            'fields': ('purchase_price', 'selling_price', 'wholesale_price', 'discount_percent', 'vat_percent')
        }),
        ('Inventory', {
            'fields': ('current_stock', 'reorder_level', 'reorder_quantity', 'unit')
        }),
        ('Regulatory', {
            'fields': ('prescription_required', 'is_controlled', 'requires_license', 'license_number')
        }),
        ('Additional', {
            'fields': ('description', 'ingredients', 'dosage', 'side_effects', 'storage_conditions', 'image')
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured', 'is_prescription')
        }),
        ('Tracking', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['product', 'movement_type', 'quantity', 'previous_quantity', 'new_quantity', 'created_at', 'created_by']
    list_filter = ['movement_type', 'created_at']
    search_fields = ['product__name', 'reference_type', 'reference_id']
    readonly_fields = ['created_at']
    list_per_page = 50


@admin.register(StockAlert)
class StockAlertAdmin(admin.ModelAdmin):
    list_display = ['product', 'alert_type', 'current_value', 'threshold_value', 'status', 'created_at']
    list_filter = ['alert_type', 'status']
    search_fields = ['product__name', 'message']
    list_per_page = 25


@admin.register(InventoryAdjustment)
class InventoryAdjustmentAdmin(admin.ModelAdmin):
    list_display = ['adjustment_number', 'product', 'reason', 'quantity', 'previous_quantity', 'new_quantity', 'created_at']
    list_filter = ['reason', 'created_at']
    search_fields = ['adjustment_number', 'product__name']
    readonly_fields = ['adjustment_number', 'previous_quantity', 'new_quantity']
    list_per_page = 25
