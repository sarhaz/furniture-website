from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from .form import UserLoginForm, UserRegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout


class UserLoginView(View):
    def get(self, request):
        form = UserLoginForm()
        context = {
            'form': form
        }
        return render(request, 'auth/login.html', context)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        data = {
            'username': username,
            'password': password
        }
        login_form = AuthenticationForm(data=data)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('index')
        else:
            form = UserRegisterForm()
            context = {
                'form': form
            }
            return render(request, 'auth/register.html', context)


class UserRegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        context = {
            'form': form
        }
        return render(request, 'auth/register.html', context)

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password_1 = request.POST.get('password_1')
        password_2 = request.POST.get('password_2')
        if password_1 == password_2:
            user = User(first_name=first_name, last_name=last_name, username=username, email=email)
            user.set_password(password_1)
            user.save()
            return redirect('login')
        else:
            return render(request, 'auth/register.html')


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')
