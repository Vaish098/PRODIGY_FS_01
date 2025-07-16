from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Registration
def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(username=username, email=email, password=password1)
                messages.success(request, "Registration successful!")
                return redirect('login')
            else:
                messages.error(request, "Username already exists.")
        else:
            messages.error(request, "Passwords do not match.")
    return render(request, 'register.html')

# Login
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, 'login.html')

# Dashboard (Protected)
@login_required(login_url='login')
def dashboard_view(request):
    return render(request, 'dashboard.html')

# Logout
def logout_view(request):
    logout(request)
    return redirect('login')
