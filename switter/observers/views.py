from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import Observer
from pages.models import PageState
from pages.utils import get_redirect_page
# Create your views here.

def add_observer(request):
    if request.method == "POST":
        observer = User.objects.get(username=request.POST['username']) 
        observed_by = User.objects.get(username=request.user)
        Observer.objects.create(observer=observer, observed_by=observed_by)

        return get_redirect_page(request.user)

def delete_observer(request):
    if request.method == "POST":
        observed_by = User.objects.get(username=request.user)
        observer = User.objects.get(username=request.POST['username'])
        print(observed_by, observer)
        Observer.objects.filter(observer=observer, observed_by=observed_by).first().delete()
    
        return get_redirect_page(request.user)

def open_observe(request):
    if request.method == "GET":
        PageState.objects.filter(user=request.user).update(sub_window='observers') 

        return get_redirect_page(request.user)

def close_observe(request):
    if request.method == "GET":
        PageState.objects.filter(user=request.user).update(sub_window=None) 
        
        return get_redirect_page(request.user)

def open_observed_by(request):
    if request.method == "GET":
    
        PageState.objects.filter(user=request.user).update(sub_window='observed_by')

        return get_redirect_page(request.user)

def close_observed_by(request):
    if request.method == "GET":
        PageState.objects.filter(user=request.user).update(sub_window=None)
        
        return get_redirect_page(request.user)