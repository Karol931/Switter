from django.shortcuts import render
from observers.utils import get_users_to_observe
from posts.utils import get_main_page_posts, check_sort_method
# Create your views here.

def main_page(request):
    if request.user.is_authenticated:
        user = request.user
        if request.session.__contains__('current_profile'):
            del request.session['current_profile']
        request.session['current_page'] = 'main_page'
        
        sort_method = check_sort_method(request.session)

        posts = get_main_page_posts(user, sort_method)
        people_to_observe = get_users_to_observe(user)
       
        return render(request, 'main_page.html', {'user' : user, 'posts': posts, 'people_to_observe': people_to_observe, 'sort_method': sort_method})
    