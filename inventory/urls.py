# inventory/urls.py

from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    # Product URLs
    path('', views.product_list_view, name='product_list'),
    path('products/', views.product_list_view, name='product_list'),
    path('products/create/', views.product_create_view, name='product_create'),
    path('products/<uuid:pk>/', views.product_detail_view, name='product_detail'),
    path('products/<uuid:pk>/update/', views.product_update_view, name='product_update'),
    path('products/<uuid:pk>/delete/', views.product_delete_view, name='product_delete'),

    # Stock URLs
    path('stock/', views.stock_list_view, name='stock_list'),
    path('stock/export-pdf/', views.export_stock_pdf_view, name='export_stock_pdf'),
    path('stock/movements/', views.stock_movement_view, name='stock_movement'),
    path('stock/movements/print/', views.stock_movement_print_view, name='stock_movement_print'),
    path('stock/adjustments/', views.stock_adjustment_view, name='stock_adjustment'),
    path('stock/alerts/', views.stock_alerts_view, name='stock_alerts'),

    # Reports
    path('reports/low-stock/', views.low_stock_report_view, name='low_stock_report'),
    path('reports/low-stock/export-pdf/', views.export_low_stock_pdf_view, name='export_low_stock_pdf'),
    path('reports/low-stock/export-excel/', views.export_low_stock_excel_view, name='export_low_stock_excel'),
    path('reports/sales/', views.sales_report_view, name='sales_report'),
    path('reports/sales/export-pdf/', views.export_sales_pdf_view, name='export_sales_pdf'),
    path('reports/sales/export-excel/', views.export_sales_excel_view, name='export_sales_excel'),

    # API URLs
    path('api/product/<uuid:product_id>/stock/', views.api_product_stock, name='api_product_stock'),
    path('api/barcode-lookup/', views.barcode_lookup_view, name='barcode_lookup'),

    # Category URLs
    path('categories/', views.category_list_view, name='category_list'),
    path('categories/create/', views.category_create_view, name='category_create'),
]