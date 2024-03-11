from django.shortcuts import render
from observers.utils import get_users_to_observe
from posts.utils import get_main_page_posts
# Create your views here.

def main_page(request):
    if request.user.is_authenticated:
        user = request.user
        request.session['current_page'] = 'main_page'
        if request.session.__contains__('sort_method'):
            sort_method = request.session['sort_method']
            posts = get_main_page_posts(user, sort_method)
        else:
            sort_method = 'newest'
            posts = get_main_page_posts(user)
        people_to_observe = get_users_to_observe(user)
       
        return render(request, 'main_page.html', {'user' : user, 'posts': posts, 'people_to_observe': people_to_observe, 'sort_method': sort_method})
    