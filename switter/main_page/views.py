from django.shortcuts import render
from django.contrib.auth.models import User
from observers.models import Observer
from posts.models import Post
from openai import OpenAI
# Create your views here.

def main_page(request):
    if request.user.is_authenticated:
        user =request.user
        posts = get_posts(user)
        people_to_observe = get_people_to_observe(user)
        return render(request, 'main_page.html', {'user' : user, 'posts': posts, 'people_to_observe': people_to_observe})
    
def get_posts(loged_in_user):
    posts = Post.objects.exclude(user=loged_in_user).order_by('-date_time')
    return posts

def get_people_to_observe(loged_in_user):
    observers = Observer.objects.filter(observed_by=loged_in_user)
    observers_ids = list(observers.values_list('observer', flat=True))
    observers_ids.append(loged_in_user.id)
    people_to_observe = User.objects.exclude(id__in=observers_ids).order_by('username')
    return people_to_observe