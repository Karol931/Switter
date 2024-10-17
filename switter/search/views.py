from django.http import HttpResponse
from django.shortcuts import render
from pages.models import PageState
from django.contrib.auth.models import User
from posts.models import Post
from django.contrib.postgres.search import TrigramSimilarity
from observers.utils import is_observed_by_check
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response


@swagger_auto_schema(method='get' ,responses={200: '', 401: 'Unauthorized'})
@api_view(['GET'])
def users(request):
    if request.user.is_authenticated:
        PageState.objects.filter(user=request.user.id).update(search_type = 'users')
        search_phrase = PageState.objects.get(user=request.user.id).search_phrase
        users = User.objects.annotate(
            similarity=TrigramSimilarity("username", search_phrase),
            ).filter(similarity__gt = 0.05).order_by('-similarity').values()
        for user in users:
            user['is_observed_by'] = is_observed_by_check(request.user, user)

        return render(request, 'search_page.html', {'search_phrase': search_phrase, 'users': users, 'logged_in_user': request.user})
    
    return Response('Unauthorized',status=401)
    

@swagger_auto_schema(method='get' ,responses={200: '', 401: 'Unauthorized'})
@api_view(['GET'])
def posts(request):
    if request.user.is_authenticated:
        PageState.objects.filter(user=request.user.id).update(search_type = 'posts')
        search_phrase = PageState.objects.get(user=request.user.id).search_phrase
        posts = Post.objects.filter(post__search = search_phrase)

        return render(request, 'search_page.html', {'search_phrase': search_phrase, 'posts': posts})
    
    return Response('Unauthorized',status=401)
