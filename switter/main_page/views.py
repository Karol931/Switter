from django.shortcuts import render
from observers.utils import get_users_to_observe
from posts.utils import get_main_page_posts
# Create your views here.

def main_page(request):
    if request.user.is_authenticated:
        user = request.user
        posts = get_main_page_posts(user)
        people_to_observe = get_users_to_observe(user)
        # likes = get_post_like_number(posts)
        return render(request, 'main_page.html', {'user' : user, 'posts': posts, 'people_to_observe': people_to_observe})
    