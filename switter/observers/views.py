from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import Observer
from pages.models import PageState
from pages.utils import get_redirect_page
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response

# Create your views here.

@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
    }
)
,responses={200: '', 401: 'Unauthorized'})
@api_view(['POST'])
def add_observer(request):
    if request.user.is_authenticated:
        username = request.data.get('username')
        observer = User.objects.get(username=username)
        observed_by = User.objects.get(username=request.user)
        Observer.objects.create(observer=observer, observed_by=observed_by)

        return get_redirect_page(request.user)

    return Response('Unauthorized',status=401)



@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
    }
)
,responses={200: '', 401: 'Unauthorized'})
@api_view(['POST'])
def delete_observer(request):
    if request.user.is_authenticated:
        username = request.data.get('username')
        observed_by = User.objects.get(username=request.user)
        observer = User.objects.get(username=username)
        print(observed_by, observer)
        Observer.objects.filter(observer=observer, observed_by=observed_by).first().delete()

        return get_redirect_page(request.user)
    
    return Response('Unauthorized',status=401)



@swagger_auto_schema(method='get' ,responses={200: '', 401: 'Unauthorized'})
@api_view(['GET'])
def open_observe(request):
    if request.user.is_authenticated:
        PageState.objects.filter(user=request.user).update(sub_window='observers') 

        return get_redirect_page(request.user)
    
    return Response('Unauthorized',status=401)



@swagger_auto_schema(method='get' ,responses={200: '', 401: 'Unauthorized'})
@api_view(['GET'])
def close_observe(request):
    if request.user.is_authenticated:
        PageState.objects.filter(user=request.user).update(sub_window=None) 
        
        return get_redirect_page(request.user)
    
    return Response('Unauthorized',status=401)



@swagger_auto_schema(method='get' ,responses={200: '', 401: 'Unauthorized'})
@api_view(['GET'])
def open_observed_by(request):
    if request.user.is_authenticated:
        PageState.objects.filter(user=request.user).update(sub_window='observed_by')

        return get_redirect_page(request.user)
    
    return Response('Unauthorized',status=401)



@swagger_auto_schema(method='get' ,responses={200: '', 401: 'Unauthorized'})
@api_view(['GET'])
def close_observed_by(request):
    if request.user.is_authenticated:
        PageState.objects.filter(user=request.user).update(sub_window=None)
        
        return get_redirect_page(request.user)
    
    return Response('Unauthorized',status=401)
