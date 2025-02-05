from functools import wraps
from django.http import HttpResponseForbidden

def premium_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_premium_active:
            return HttpResponseForbidden("This feature requires an active premium subscription")
        return view_func(request, *args, **kwargs)
    return wrapper



def set_coop_header(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        response['Cross-Origin-Opener-Policy'] = 'same-origin-allow-popups'
        return response
    return _wrapped_view

