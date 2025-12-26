import threading

_user = threading.local()

class CurrentUserMiddleware:
    """
    Save current user in thread local storage so we can access it in signals.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _user.value = getattr(request, 'user', None)
        response = self.get_response(request)
        return response

def get_current_user():
    return getattr(_user, 'value', None)