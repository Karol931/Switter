from django.shortcuts import render
from observers.utils import get_users_to_observe, get_users_observed_by, get_observers_of_user, get_observed_by_count, get_observer_of_count
from posts.utils import get_main_page_posts, get_profile_page_posts, check_sort_method
from django.contrib.auth.models import User
from .models import PageState
from pages.utils import is_same_profile, load_sub_window_data
from search.utils import search
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
# Create your views here.

@swagger_auto_schema(method='get' ,responses={200: '', 401: 'Unauthorized'})
@api_view(['GET'])
def main_page(request):
    if request.user.is_authenticated:
        user = request.user
        PageState.objects.filter(user=user).update(page='main_page', profile=None, sub_window=None, search_phrase=None)
        
        sort_method = check_sort_method(user)

        posts = get_main_page_posts(user)
        people_to_observe = get_users_to_observe(user)
    
        return render(request, 'main_page.html', {'user' : user, 'posts': posts, 'people_to_observe': people_to_observe, 'sort_method': sort_method})
        
    return render(request, 'login.html')


@swagger_auto_schema(method='get' ,responses={200: '', 401: 'Unauthorized'})
@api_view(['GET'])
def profile_page(request, username):
    if request.user.is_authenticated:
        logged_in_user = request.user
        if is_same_profile(username, logged_in_user):
            PageState.objects.filter(user=logged_in_user).update(page='profile_page', profile=username, search_phrase=None)
        else:
            PageState.objects.filter(user=logged_in_user).update(page='profile_page', profile=username, sub_window=None, search_phrase=None)
        
        page_state = PageState.objects.get(user=logged_in_user)
        
        user_of_profile = User.objects.get(username = username)
        
        observed_by_count, observer_count = get_observed_by_count(user_of_profile), get_observer_of_count(user_of_profile)
        
        observer_or_observed_by = load_sub_window_data(page_state.sub_window, user_of_profile, logged_in_user)
        
        sort_method = check_sort_method(logged_in_user)
        posts = get_profile_page_posts(user_of_profile, logged_in_user)

        return render(request, 'profile_page.html', {'logged_in_user': logged_in_user, 'posts': posts, 'sort_method': sort_method, 'user_of_profile': user_of_profile, 'opened_sub_window': page_state.sub_window, 'observer_or_observed_by': observer_or_observed_by, 'observed_by_count': observed_by_count, 'observer_count': observer_count})
    
    return Response('Unauthorized',status=401)


@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'search': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
    }
)
,responses={200: '', 401: 'Unauthorized'})
@swagger_auto_schema(method='get' ,responses={200: '', 401: 'Unauthorized'})
@api_view(['GET', 'POST'])
def search_page(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user = request.user
            PageState.objects.filter(user=user).update(page='search_page', profile=None, sub_window=None)
            search_phrase = PageState.objects.get(user=request.user.id).search_phrase
            print(search_phrase)
            
            return render(request, 'search_page.html', {'search_phrase': search_phrase})
        
        return Response('Unauthorized',status=401)
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            return search(request)
    
        return Response('Unauthorized',status=401)