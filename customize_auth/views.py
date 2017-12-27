from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .models import User


class Login(View):
    def get(self, request):
        return HttpResponse('login get')

    def post(self, request):
        user = User.objects.filter(name=request.POST.get('username')).first()
        if not user:
            return HttpResponseNotFound('No such user')
        if not user.verify_password(request.POST.get('password')):
            return redirect('login')
        login(request, user)
        return HttpResponse('login post')


class Logout(View):
    def get(self, request):
        logout(request)
        return HttpResponse('logout')


@login_required
def test(request):
    return HttpResponse('test')
