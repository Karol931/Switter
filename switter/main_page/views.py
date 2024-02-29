from django.shortcuts import render
from django.contrib.auth.models import User
from posts.models import Post

# Create your views here.

def main_page(request):
    if request.user.is_authenticated:
        username =request.user
        posts = get_posts()
        return render(request, 'main_page.html', {'username' : username, 'posts': posts})
    
def get_posts():
    posts = Post.objects.all().order_by('-date_time')
    return posts