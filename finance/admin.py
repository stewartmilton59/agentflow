from django.contrib import admin

from .models import Expense, ExpenseCategory


@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_frequent', 'is_active', 'color', 'created_at']
    list_filter = ['is_frequent', 'is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 25


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['expense_number', 'category', 'description', 'amount', 'expense_date', 'payment_method', 'paid_to', 'created_by']
    list_filter = ['category', 'payment_method', 'expense_date']
    search_fields = ['expense_number', 'description', 'paid_to', 'reference_number']
    readonly_fields = ['expense_number', 'created_at', 'updated_at']
    date_hierarchy = 'expense_date'
    list_per_page = 50

    fieldsets = (
        ('Expense Details', {
            'fields': ('expense_number', 'category', 'description', 'amount', 'expense_date', 'payment_method', 'paid_to', 'reference_number', 'notes')
        }),
        ('Tracking', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )
