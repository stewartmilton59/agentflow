from django.urls import path

from . import views

app_name = 'finance'

urlpatterns = [
    path('', views.finance_dashboard_view, name='dashboard'),
    path('dashboard/', views.finance_dashboard_view, name='dashboard'),

    path('expenses/', views.expense_list_view, name='expense_list'),
    path('expenses/add/', views.expense_create_view, name='expense_create'),
    path('expenses/delete/<uuid:expense_id>/', views.expense_delete_view, name='expense_delete'),
    path('expenses/ajax-add/', views.expense_quick_add_ajax_view, name='expense_quick_add'),

    path('categories/', views.expense_category_list_view, name='expense_category_list'),
    path('categories/add/', views.expense_category_list_view, name='expense_category_create'),
    path('categories/<uuid:category_id>/edit/', views.expense_category_edit_view, name='expense_category_edit'),
    path('categories/<uuid:category_id>/delete/', views.expense_category_delete_view, name='expense_category_delete'),
    path('categories/<uuid:category_id>/expenses/', views.expense_category_expenses_view, name='expense_category_expenses'),
]
