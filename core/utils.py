"""Utility functions for the core app."""
from .models import ActivityLog


def get_client_ip(request):
    """Get the client's IP address from the request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', '')
    return ip


def get_user_agent(request):
    """Get the client's user agent from the request."""
    return request.META.get('HTTP_USER_AGENT', '')[:512]


def log_activity(user, category, action, description='', request=None, **kwargs):
    """
    Log user activity.
    
    Args:
        user: User instance
        category: One of: 'security', 'progress', 'quiz', 'game', 'profile', 'content', 'download', 'system'
        action: One of the ACTION_CHOICES from ActivityLog model
        description: Optional text description
        request: Optional request object to extract IP and user agent
        **kwargs: Additional fields (article, quiz_id, game_id, media, metadata)
    
    Returns:
        ActivityLog instance
    """
    log_data = {
        'user': user,
        'category': category,
        'action': action,
        'description': description,
    }
    
    # Add IP and user agent if request is provided
    if request:
        log_data['ip_address'] = get_client_ip(request)
        log_data['user_agent'] = get_user_agent(request)
    
    # Add optional fields
    for key in ['article', 'quiz_id', 'game_id', 'media', 'metadata']:
        if key in kwargs:
            log_data[key] = kwargs[key]
    
    return ActivityLog.objects.create(**log_data)
