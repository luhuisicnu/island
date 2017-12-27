from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import Login, Logout, test

urlpatterns = [
    path('login', csrf_exempt(Login.as_view()), name='login'),
    path('logout', csrf_exempt(Logout.as_view()), name='logout'),
    path('test', test),
]
