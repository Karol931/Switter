from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import Observer
# Create your views here.

def add_observer(request):
    if request.method == "POST":
        observer = User.objects.get(username=request.POST['username']) 
        observed_by = User.objects.get(username=request.user)
        Observer.objects.create(observer=observer, observed_by=observed_by)
    
    if request.session['current_page'] == 'main_page':
        return redirect(request.session['current_page'])
    return redirect(request.session['current_page'], username=request.session['current_profile'])

def delete_observer(request):
    if request.method == "POST":
        observed_by = User.objects.get(username=request.user)
        observer = User.objects.get(username=request.POST['username'])
        print(observed_by, observer)
        Observer.objects.filter(observer=observer, observed_by=observed_by).first().delete()
    
    if request.session['current_page'] == 'main_page':
        return redirect(request.session['current_page'])
    return redirect(request.session['current_page'], username=request.session['current_profile'])

def open_observe(request):
    if request.method == "GET":
        request.session['open_observer'] = True
        
        if request.session['current_page'] == 'main_page':
            return redirect(request.session['current_page'])
        return redirect(request.session['current_page'], username=request.session['current_profile'])

def close_observe(request):
    if request.method == "GET":
        del request.session['open_observer']

        if request.session['current_page'] == 'main_page':
            return redirect(request.session['current_page'])
        return redirect(request.session['current_page'], username=request.session['current_profile'])

def open_observed_by(request):
    if request.method == "GET":
        request.session['open_observed_by'] = True

        if request.session['current_page'] == 'main_page':
            return redirect(request.session['current_page'])
        return redirect(request.session['current_page'], username=request.session['current_profile'])

def close_observed_by(request):
    if request.method == "GET":
        del request.session['open_observed_by']
        
        if request.session['current_page'] == 'main_page':
            return redirect(request.session['current_page'])
        return redirect(request.session['current_page'], username=request.session['current_profile'])