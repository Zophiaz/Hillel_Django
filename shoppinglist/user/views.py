from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import defaults
import django.views.defaults
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import uuid
from slist.models import UserToList


def index(request):
    if not request.user.is_authenticated:
        return HttpResponse('You are not logged in')
    user_id = request.user.id
    user_list = UserToList.objects.filter(user_id=user_id).first()
    return render(request, 'user_index.html')


def invite_user(request):
    if not request.user.is_authenticated:
        return HttpResponse('You are not logged in')
    if request.method == 'GET':
        return render(request, 'invite_form.html')

    email = request.POST.get('email')
    invited_user = User.objects.filter(email=email).first()
    if invited_user is None:
        return HttpResponse("User is not found")
    invited_user_list = UserToList.objects.filter(user_id=invited_user.id).first()
    current_user_list = UserToList.objects.filter(user_id=request.user.id).first()
    invited_user_list.list_id = current_user_list.list_id
    invited_user_list.save()
    return HttpResponse(f'User {invited_user.email} is invited')


def register_user(request):
    if request.user.is_authenticated:
        return HttpResponse('You are already logged in. Please go back to previous page.')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create_user(username, email, password)
        user.save()
        user_list = UserToList(user_id=user.id, list_id=uuid.uuid4())
        user_list.save()
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
