from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Observer
# Create your views here.

def add_observer(request):
    if request.method == "POST":
        observer = User.objects.get(username=request.POST['username']) 
        observed_by = User.objects.get(username=request.user)
        Observer.objects.create(observer=observer, observed_by=observed_by)
    return redirect('main_page')

def delete_observer(request):
    return