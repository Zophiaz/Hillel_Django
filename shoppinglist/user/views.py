from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import defaults
import django.views.defaults
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def index(request):
    return render(request, 'user_index.html')


def register_user(request):
    if request.user.is_authenticated:
        return HttpResponse('You are already logged in. Please go back to previous page.')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create_user(username, email, password)
        user.save()
        return redirect('http://127.0.0.1:8000/user/login/')
    return render(request, 'register_form.html')


def login_user(request):
    if request.user.is_authenticated:
        return HttpResponse('You are already logged in. Please go back to previous page.')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse('You are logged in. Please go back to previous page.')
        else:
            return HttpResponse('You are not logged in. Please go back to previous page.')
    else:
        return render(request, 'login_form.html')


def logout_user(request):
    logout(request)
    return redirect('http://127.0.0.1:8000/user/login/')
