from django.http import HttpResponse
from django.shortcuts import render
from pages.models import PageState
from django.contrib.auth.models import User


def users(request):
    if request.method == 'GET':
        PageState.objects.filter(user=request.user.id).update(search_type = 'users')
        page_state = PageState.objects.get(user=request.user.id)
        users = User.objects.filter(username__search=request.user.username)
        for user in users:
            print(user.username)
        return render(request, 'search_page.html', {})
    

def posts(request):
    if request.method == 'GET':
        PageState.objects.filter(user=request.user.id).update(search_type = 'posts')
        page_state = PageState.objects.get(user=request.user.id)
        return render(request, 'search_page.html', {})