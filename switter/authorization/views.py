from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from pages.models import PageState
# Create your views here.

def login_user(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('main_page')
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if PageState.objects.get(user=user.id) is not None:
                PageState.objects.get(user=user.id).delete()
            PageState.objects.create(user=user)
            login(request, user)
            return redirect('main_page')

        else:
            messages.error(request, 'User with those credentials doesn\'t exist.')
            return render(request, 'login.html')

def register_user(request):
    if request.method == 'GET':
       return render(request, 'register.html')
    elif request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        password_confirmation = request.POST['password_confirmation']

        if password != password_confirmation:
            messages.error(request, 'Passwords don\'t match.')
            return render(request, 'register.html')
        try:
            User.objects.create_user(username=username, email=email, password=password, first_name=fname, last_name=lname)
        except:
            messages.error(request, 'Username already taken.')
            return render(request, 'register.html')
        messages.success(request, 'Succesfuly created an account')
        return redirect('login')
    
def logout_user(request):
    if request.method == 'GET':
        PageState.objects.get(user=request.user).delete()
        logout(request)
        return redirect('login')