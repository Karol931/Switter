from django.shortcuts import render
from observers.utils import get_users_observers
from posts.utils import get_logged_in_user_posts

def profile_page(request):
    if request.method == 'GET':
        user = request.user
        request.session['current_page'] = 'profile_page'
        posts = get_logged_in_user_posts(user)
        observers = get_users_observers(user)
        
        return render(request, 'profile_page.html', {'user': user, 'posts': posts, 'observers': observers})