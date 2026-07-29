from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from .models import UserActivityLog

class ActivityLogMiddleware(MiddlewareMixin):
    """Track user activity"""

    def process_request(self, request):
        if request.user.is_authenticated:
            # Update last activity
            request.user.last_activity = timezone.now()
            request.user.save(update_fields=['last_activity'])

            # Track page views (optional)
            if request.method == 'GET' and not request.path.startswith('/static/'):
                UserActivityLog.objects.create(
                    user=request.user,
                    action='view',
                    description=f'Visited {request.path}',
                    ip_address=request.META.get('REMOTE_ADDR'),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )