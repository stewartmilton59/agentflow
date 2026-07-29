# core/decorators.py
from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect

def administrator_required(view_func):
    """Decorator to restrict access to administrators only"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please login to continue.')
            return redirect('login')

        # Check if user is admin or superuser
        is_admin = getattr(request.user, 'is_administrator', False) or request.user.is_superuser

        if not is_admin:
            messages.error(
                request,
                'Access Denied. The dashboard is only available to administrators.'
            )
            # Redirect to a page that DOES NOT have this decorator
            return redirect('sales:pos_view')  # POS page - no admin check

        return view_func(request, *args, **kwargs)
    return wrapper