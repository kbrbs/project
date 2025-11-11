"""
Access control utilities for public vs authenticated users.

Public users get limited access to encourage registration:
- 3 games total (rest require login to play)
- Unlimited quiz access
- Full lesson viewing access
- Festival tour viewing (no interactive features)
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


# Public access limits
PUBLIC_GAMES_LIMIT = 3  # Total playable games for public users
PUBLIC_QUIZZES_LIMIT = None  # Unlimited quiz access for public
PUBLIC_LESSONS_PREVIEW = False  # Full lesson access for public


def limit_public_access(queryset, user, limit=3):
    """
    Limit queryset for public (anonymous) users.
    Authenticated users get full access.
    
    Args:
        queryset: Django queryset to limit
        user: Request user object
        limit: Number of items to show for public users (default 3)
    
    Returns:
        Limited or full queryset based on authentication
    """
    if user.is_authenticated:
        return queryset
    return queryset[:limit]


def require_login_for_feature(feature_name="this feature"):
    """
    Decorator to require login for specific features.
    Shows a friendly message and redirects to login.
    
    Args:
        feature_name: Name of the feature requiring login (for message)
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.info(
                    request,
                    f'Please register or log in to access {feature_name}. '
                    f'Create your free account to unlock all games, quizzes, and learning resources!'
                )
                return redirect(f'/accounts/login/?next={request.path}')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def get_public_access_context(user):
    """
    Get context data about access limits for templates.
    
    Returns dict with:
        - user_is_authenticated: boolean
        - games_limit: int or None
        - quizzes_limit: int or None
        - has_full_access: boolean
    """
    return {
        'user_is_authenticated': user.is_authenticated,
        'games_limit': None if user.is_authenticated else PUBLIC_GAMES_LIMIT,
        'quizzes_limit': None if user.is_authenticated else PUBLIC_QUIZZES_LIMIT,
        'has_full_access': user.is_authenticated,
        'show_registration_prompt': not user.is_authenticated,
    }
