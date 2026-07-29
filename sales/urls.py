# sales/urls.py

from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    # POS URLs
    path('', views.pos_table_view, name='pos_table'),
    path('pos/', views.pos_view, name='pos_view'),
    path('pos-table/', views.pos_table_view, name='pos_table'),

    # SALE endpoint (real sales only - affects stock)
    path('pos/save-sale/', views.pos_save_sale, name='pos_save_sale'),

    # PROFORMA endpoint (quotations only - NO stock impact)
    path('pos/save-proforma/', views.pos_save_proforma, name='pos_save_proforma'),

    path('pos/cart/', views.get_cart, name='get_cart'),
    path('pos/add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('pos/update-cart/', views.update_cart, name='update_cart'),
    path('pos/remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
    path('pos/clear-cart/', views.clear_cart, name='clear_cart'),
    path('pos/checkout/', views.checkout_view, name='checkout'),

    # API URLs
    path('api/products/', views.api_products, name='api_products'),
    path('api/products/<uuid:product_id>/stock/', views.api_product_stock, name='api_product_stock'),

    # Proforma URLs
    path('proformas/', views.proforma_list_view, name='proforma_list'),
    path('proformas/<uuid:pk>/print/', views.proforma_receipt_view, name='proforma_receipt'),
    path('proformas/<uuid:pk>/convert/', views.convert_proforma_to_sale_view, name='convert_proforma'),

    # Sale URLs
    path('sales/', views.sale_list_view, name='sale_list'),
    path('sales/<uuid:pk>/', views.sale_detail_view, name='sale_detail'),
    path('sales/<uuid:pk>/receipt/', views.sale_receipt_view, name='sale_receipt'),
    path('sales/<uuid:pk>/delivery-note/', views.delivery_note_view, name='sale_delivery_note'),
    path('sales/<uuid:pk>/payments/', views.sale_payments_view, name='sale_payments'),
    path('sales/<uuid:pk>/add-payment/', views.add_partial_payment, name='add_partial_payment'),
    path('sales/<uuid:pk>/update/', views.sale_update_view, name='sale_update'),
    path('sales/<uuid:pk>/delete/', views.sale_delete_view, name='sale_delete'),

    # Payment URLs
    path('payments/<uuid:pk>/edit/', views.edit_payment_view, name='edit_payment'),
    path('payments/<uuid:pk>/delete/', views.delete_payment_view, name='delete_payment'),

    # Customer URLs
    path('customers/', views.customer_list_view, name='customer_list'),
    path('customers/create/', views.customer_create_view, name='customer_create'),
    path('customers/<uuid:pk>/', views.customer_detail_view, name='customer_detail'),

    # Credit URLs
    path('credits/', views.credit_list_view, name='credit_list'),
    path('credits/<uuid:pk>/', views.credit_detail_view, name='credit_detail'),
    path('credits/<uuid:pk>/pay/', views.credit_payment_view, name='credit_payment'),
]