from functools import wraps

from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject
from django.conf import settings
from django.contrib.auth.models import AnonymousUser

from .models import User

UID_KEY = '_auth_user_id'


def login_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.session.get(UID_KEY):
            return func(request, *args, **kwargs)
        else:
            from django.contrib.auth.views import redirect_to_login
            path = request.get_full_path()
            return redirect_to_login(path)
    return wrapper


def login(request, user):
    request.session[UID_KEY] = user.id


def logout(request):
    request.session.flush()


def get_user(request):
    if not request.session.get(UID_KEY):
        return AnonymousUser()

    return User.objects.get(pk=request.session.get(UID_KEY))


class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        assert hasattr(request, 'session'), (
            "The customize authentication middleware requires session middleware "
            "to be installed. Edit your MIDDLEWARE%s setting to insert "
            "'django.contrib.sessions.middleware.SessionMiddleware' before "
            "'customize_auth.login_management.AuthenticationMiddleware'."
        ) % ("_CLASSES" if settings.MIDDLEWARE is None else "")
        request.customize_user = SimpleLazyObject(lambda: get_user(request))
