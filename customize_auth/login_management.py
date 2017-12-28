from functools import wraps
from django.contrib.auth import SESSION_KEY


def login_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.session.get(SESSION_KEY):
            return func(request, *args, **kwargs)
        else:
            from django.contrib.auth.views import redirect_to_login
            path = request.get_full_path()
            return redirect_to_login(path)
    return wrapper
