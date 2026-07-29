from django.urls import path
from . import views

app_name = 'purchases'

urlpatterns = [
    # Purchase Order URLs
    path('', views.purchase_order_list_view, name='purchase_order_list'),
    path('orders/', views.purchase_order_list_view, name='purchase_order_list'),
    path('orders/create/', views.purchase_order_create_view, name='purchase_order_create'),
    path('orders/<uuid:pk>/', views.purchase_order_detail_view, name='purchase_order_detail'),
    path('orders/<uuid:pk>/cancel/', views.purchase_order_cancel_view, name='purchase_order_cancel'),
    path('orders/<uuid:pk>/pdf/', views.purchase_order_pdf_view, name='purchase_order_pdf'),
]