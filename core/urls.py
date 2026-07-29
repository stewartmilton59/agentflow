from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # path('', views.dashboard_view, name='dashboard'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('settings/company/', views.company_settings_view, name='company_settings'),
    path('settings/payment-method/ajax/', views.payment_method_ajax_view, name='payment_method_ajax'),
    path('settings/system/', views.system_settings_view, name='system_settings'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/read/<uuid:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('activity-logs/', views.activity_logs_view, name='activity_logs'),
    path('activity-logs/delete-all/', views.delete_all_activity_logs, name='delete_all_activity_logs'),
    path('activity-logs/delete-old/', views.delete_old_activity_logs, name='delete_old_activity_logs'),
    path('activity-logs/export/', views.export_activity_logs, name='export_activity_logs'),
    path('backup/', views.backup_view, name='backup'),
    path('backup/delete/<uuid:backup_id>/', views.delete_backup, name='delete_backup'),
]