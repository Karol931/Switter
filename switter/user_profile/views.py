from django.shortcuts import render
from posts.models import Post
from observers.models import Observer
from django.contrib.auth.models import User

def profile_page(request):
    if request.method == 'GET':
        user = request.user
        posts = get_user_posts(user)
        observers = get_users_observers(user)
        return render(request, 'profile_page.html', {'user': user, 'posts': posts, 'observers': observers})


def get_user_posts(user):
    posts = Post.objects.filter(user=user).order_by('-date_time')
    print(posts)
    return posts


def get_users_observers(user):
    observers = Observer.objects.filter(observed_by=user.id)
    observers_ids = observers.values_list('observer', flat=True)
    observers = User.objects.filter(id__in=observers_ids).order_by('username')
    return observers