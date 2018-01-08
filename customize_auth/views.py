from datetime import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import User
from .forms import LoginForm, RegisterForm, UserForm
from .login_management import login_required, login, logout, UID_KEY


class Register(View):
    def get(self, request):
        context = {"form": RegisterForm()}
        return render(request, 'customize_auth/register.html', context=context)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            User.objects.create(name=form.cleaned_data['username'], password=form.cleaned_data['password'])
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
            return redirect(request.GET.get('next') or 'test')

        context = {"form": form}
        return render(request, 'customize_auth/login.html', context=context)


@method_decorator(login_required, name='dispatch')
class Logout(View):
    def get(self, request):
        logout(request)
        return redirect(request.GET.get('next') or 'test')


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
        file = request.FILES.get('avatar')
        if not file:
            return HttpResponseBadRequest('No file named avatar upload!')


@login_required
def test(request):
    print(request.customize_user)
    return render(request, 'base.html')
