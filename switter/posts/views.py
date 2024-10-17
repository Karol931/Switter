from django.shortcuts import redirect
from .models import Post, Like
from datetime import datetime
from django.contrib import messages
from .utils import check_post_sentiment
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
        'new-post': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
    }
)
,responses={200: '', 401: 'Unauthorized'})
@api_view(['POST'])
def add_post(request):
    if request.user.is_authenticated:
        new_post = request.data.get('new-post')
        if check_post_sentiment(new_post) == 'positive':
            user = request.user
            date_time = datetime.now()
            Post.objects.create(user=user, post=new_post, date_time=date_time)
            messages.success(request, 'Tweet added succesfully.')
        else:
            messages.error(request, 'Tweet didn\'t match our standards.')
        
        return get_redirect_page(request.user)

    return Response('Unauthorized',status=401)

   

@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'post-id': openapi.Schema(type=openapi.TYPE_INTEGER, description='int'),
    }
)
,responses={200: '', 401: 'Unauthorized'})
@api_view(['POST'])
def delete_post(request):
    if request.user.is_authenticated:
        post_id = request.data.get('post-id')
        print(post_id)
        Post.objects.get(id=post_id).delete()

        return get_redirect_page(request.user)

    return Response('Unauthorized',status=401)



@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'post-id': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
    }
)
,responses={200: '', 401: 'Unauthorized'})
@api_view(['POST'])
def add_like(request):
    if request.user.is_authenticated:
        user = request.user
        post_id = request.data.get('post-id')
        post = Post.objects.get(id=post_id)
        Like.objects.create(user=user, post=post)
        
        return get_redirect_page(request.user)

    return Response('Unauthorized',status=401)



@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'post-id': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
    }
)
,responses={200: '', 401: 'Unauthorized'})
@api_view(['POST'])
def delete_like(request):
    if request.user.is_authenticated:
        user = request.user
        post_id = request.data.get('post-id')
        post = Post.objects.get(id=post_id)
        Like.objects.get(post=post, user=user).delete()
        
        return get_redirect_page(request.user)

    return Response('Unauthorized',status=401)



@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'sort-method': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
    }
)
,responses={200: '', 401: 'Unauthorized'})
@api_view(['POST'])
def set_sort_method(request):
    if request.user.is_authenticated:
        page_state = PageState.objects.filter(user=request.user)        
        sort_method = request.data.get('sort-method')
        page_state.update(sort_method=sort_method)

        return get_redirect_page(request.user)
    
    return Response('Unauthorized',status=401)
