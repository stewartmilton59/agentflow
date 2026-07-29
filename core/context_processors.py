from .models import Company, Notification
from accounts.permissions import has_permission, can_access_page

def system_settings(request):
    """Make system settings available to all templates"""
    company = Company.objects.first()
    unread_notifications_count = 0

    if request.user.is_authenticated:
        unread_notifications_count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()

    return {
        'company': company,
        'unread_notifications_count': unread_notifications_count,
    }


# permissions

def user_permissions(request):
    """Make user permissions available in all templates"""
    if not request.user.is_authenticated:
        return {}

    return {
        'user_role': request.user.role,
        'user_is_admin': request.user.role == 'admin' or request.user.is_superuser,
        'user_is_manager': request.user.role == 'manager',
        'user_is_pharmacist': request.user.role == 'pharmacist',
        'user_is_cashier': request.user.role == 'cashier',
        'user_is_auditor': request.user.role == 'auditor',
        'user_is_saler': request.user.role == 'saler',
        'can_view_sales': has_permission(request.user, 'can_view_all_sales') or has_permission(request.user, 'can_view_own_sales_only'),
        'can_manage_inventory': has_permission(request.user, 'can_manage_inventory'),
        'can_manage_users': has_permission(request.user, 'can_manage_users'),
        'can_view_reports': has_permission(request.user, 'can_view_reports'),
        'can_view_activity_logs': has_permission(request.user, 'can_view_activity_logs'),
    }