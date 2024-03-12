from django.shortcuts import render
from observers.utils import get_users_observed_by, get_observers_of_user, get_observed_by_count, get_observer_of_count
from posts.utils import get_profile_page_posts, check_sort_method
from django.contrib.auth.models import User

def profile_page(request, username):
    if request.method == 'GET':
        logged_in_user = request.user
        
        request.session['current_page'] = 'profile_page'
        request.session['current_profile'] = username
        
        user_of_profile = User.objects.get(username = username)
        
        observer_or_observed_by = None
        opened_sub_window = None
        observed_by_count, observer_count = get_observed_by_count(user_of_profile), get_observer_of_count(user_of_profile)

        if request.session.__contains__('open_observer'):
            opened_sub_window = 'open_observer'
            observer_or_observed_by = get_observers_of_user(request.user, user_of_profile)
        elif request.session.__contains__('open_observed_by'):
            opened_sub_window = 'open_observed_by'
            observer_or_observed_by = get_users_observed_by(request.user, user_of_profile)

        sort_method = check_sort_method(request.session)
        posts = get_profile_page_posts(user_of_profile, logged_in_user, sort_method)

        return render(request, 'profile_page.html', {'logged_in_user': logged_in_user, 'posts': posts, 'sort_method': sort_method, 'user_of_profile': user_of_profile, 'opened_sub_window': opened_sub_window, 'observer_or_observed_by': observer_or_observed_by, 'observed_by_count': observed_by_count, 'observer_count': observer_count})