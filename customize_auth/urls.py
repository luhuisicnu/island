from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import Login, Logout, test, Register

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('', test, name='test'),
]
