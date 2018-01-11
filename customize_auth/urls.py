from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import Login, Logout, Register, Profile, UserEdit, UploadAvatar

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('profile/', Profile.as_view(), name='profile'),
    path('user-edit/', UserEdit.as_view(), name='user_edit'),
    path('upload-avatar/', UploadAvatar.as_view(), name='upload_avatar'),
]


