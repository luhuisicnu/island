from datetime import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import User, Level
from .forms import LoginForm, RegisterForm, UserForm, AvatarForm
from .login_management import login_required, login, logout, UID_KEY


class Register(View):
    def get(self, request):
        context = {"form": RegisterForm()}
        return render(request, 'customize_auth/register.html', context=context)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create(name=form.cleaned_data['username'], password=form.cleaned_data['password'])
            Level.objects.create(user=new_user, name=new_user.name, description=settings.LEVEL_NAME[0])
            return redirect('login')

        context = {"form": form}
        return render(request, 'customize_auth/register.html', context=context)


class Login(View):
    def get(self, request):
        context = {"form": LoginForm()}
        return render(request, 'customize_auth/login.html', context=context)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = User.objects.filter(name=form.cleaned_data['username']).first()
            login(request, user)
            user.last_login = datetime.now()
            user.save()
            return redirect(request.GET.get('next') or 'index')

        context = {"form": form}
        return render(request, 'customize_auth/login.html', context=context)


@method_decorator(login_required, name='dispatch')
class Logout(View):
    def get(self, request):
        logout(request)
        return redirect(request.GET.get('next') or 'index')


@method_decorator(login_required, name='dispatch')
class Profile(View):
    def get(self, request):
        return render(request, 'customize_auth/profile.html')


@method_decorator(login_required, name='dispatch')
class UserEdit(View):
    def get(self, request):
        context = {'form': UserForm(instance=request.customize_user)}
        return render(request, 'customize_auth/user_edit.html', context=context)

    def post(self, request):
        form = UserForm(request.POST, request.FILES, instance=request.customize_user)
        if form.is_valid():
            form.save()
            return redirect(request.GET.get('next') or 'profile')

        context = {"form": form}
        return render(request, 'customize_auth/user_edit.html', context=context)


@method_decorator(login_required, name='dispatch')
class UploadAvatar(View):
    def post(self, request):
        form = AvatarForm(request.POST, request.FILES, instance=request.customize_user)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        return HttpResponseBadRequest(str(form.errors))
