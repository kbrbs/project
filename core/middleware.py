from .models import Visit
from django.utils.deprecation import MiddlewareMixin


class AnalyticsMiddleware(MiddlewareMixin):
    """Simple middleware to log GET page visits into Visit model for analytics.

    Note: keep this lightweight to avoid performance issues in production.
    """

    def process_request(self, request):
        try:
            if request.method == 'GET' and not request.path.startswith('/static/') and not request.path.startswith('/media/'):
                ip = request.META.get('REMOTE_ADDR', '')
                ua = request.META.get('HTTP_USER_AGENT', '')[:512]
                Visit.objects.create(path=request.path, user=getattr(request, 'user', None) if request.user.is_authenticated else None, ip_address=ip, user_agent=ua)
        except Exception:
            # Don't fail requests if analytics logging fails
            pass
