from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.views import View
from django.contrib.auth.models import User as auth_user
from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import login, logout
from .models import User
from .forms import LoginForm, RegisterForm
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
            return redirect(request.GET.get('next') or 'test')

        context = {"form": form}
        return render(request, 'customize_auth/login.html', context=context)


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect(request.GET.get('next') or 'test')


@login_required
def test(request):
    print(request.customize_user)
    return render(request, 'base.html')
