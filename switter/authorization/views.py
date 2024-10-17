from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from pages.models import PageState
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Create your views here.


@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
    }
)
,responses={200: '', 400: 'User with those credentials doesn\'t exist.'})
@swagger_auto_schema(method='get' ,responses={200: ''})
@api_view(['GET', 'POST'])
def login_user(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('main_page')
        
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if PageState.objects.filter(user=user.id):
                PageState.objects.get(user=user.id).delete()
            PageState.objects.create(user=user)
            login(request, user)

            return redirect('main_page')
        else:
            messages.error(request, 'User with those credentials doesn\'t exist.')

            return render(status=400, request=request, template_name='login.html')


@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'fname': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'lname': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'email': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'password_confirmation': openapi.Schema(type=openapi.TYPE_STRING, description='string'),

    }
)
,responses={200: '', 400: 'Passwords don\'t match.', 400: 'Username already taken.'})
@swagger_auto_schema(method='get' ,responses={200: ''})
@api_view(['GET', 'POST'])
def register_user(request):
    if request.method == 'GET':
       return render(request, 'register.html')
    elif request.method == 'POST':
        username = request.data.get('username')
        fname = request.data.get('fname')
        lname = request.data.get('lname')
        email = request.data.get('email')
        password = request.data.get('password')
        password_confirmation = request.data.get('password_confirmation')

        if password != password_confirmation:
            messages.error(request, 'Passwords don\'t match.')
            
            return render(status=400, request=request, template_name='register.html')
        try:
            User.objects.create_user(username=username, email=email, password=password, first_name=fname, last_name=lname)
        except:
            messages.error(request, 'Username already taken.')
            
            return render(status=400, request=request, template_name='register.html')
        messages.success(request, 'Succesfuly created an account.')
        
        return redirect('login')


@swagger_auto_schema(method='get' ,responses={200: ''})
@api_view(['GET'])
def logout_user(request):
    if request.user.is_authenticated:
        PageState.objects.get(user=request.user).delete()
        logout(request)
    
    return redirect('login')