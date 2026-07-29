from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from accounts.permissions import can_access_page, has_permission

def role_required(allowed_roles):
    """Decorator to check if user has allowed role"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')

            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            if hasattr(request.user, 'role') and request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)

            messages.error(request, 'You do not have permission to access this page.')
            return redirect('core:dashboard')
        return wrapper
    return decorator

def permission_required(permission):
    """Decorator to check if user has specific permission"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')

            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            if has_permission(request.user, permission):
                return view_func(request, *args, **kwargs)

            messages.error(request, f'You need {permission} permission to access this page.')
            return redirect('core:dashboard')
        return wrapper
    return decorator

def page_required(page_name):
    """Decorator to check if user can access specific page"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')

            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            if can_access_page(request.user, page_name):
                return view_func(request, *args, **kwargs)

            messages.error(request, 'You do not have permission to access this page.')
            return redirect('core:dashboard')
        return wrapper
    return decorator

# Specific role decorators
def admin_required(view_func):
    return role_required(['admin'])(view_func)

def manager_required(view_func):
    return role_required(['admin', 'manager'])(view_func)

def pharmacist_required(view_func):
    return role_required(['admin', 'manager', 'pharmacist'])(view_func)

def cashier_required(view_func):
    return role_required(['admin', 'manager', 'pharmacist', 'cashier'])(view_func)

def auditor_required(view_func):
    return role_required(['admin', 'auditor'])(view_func)

def saler_required(view_func):
    return role_required(['admin', 'manager', 'saler'])(view_func)