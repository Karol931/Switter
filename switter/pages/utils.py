from django.shortcuts import redirect
from pages.models import PageState
from observers.utils import get_users_observed_by, get_observers_of_user

def get_redirect_page(user):

    page_state = PageState.objects.get(user=user)

    if page_state.page == 'main_page':
        return redirect('main_page')
    elif page_state.page == 'profile_page':
        return redirect('profile_page', username=page_state.profile)
    

def is_same_profile(username, logged_in_user):
    old_profile = PageState.objects.get(user=logged_in_user).profile
    if old_profile == username:
        return True
    
    return False

def load_sub_window_data(sub_window, user_of_profile, logged_in_user):
    
    if sub_window == 'observers':
        observer_or_observed_by = get_observers_of_user(logged_in_user, user_of_profile)
    elif sub_window == 'observed_by':
        observer_or_observed_by = get_users_observed_by(logged_in_user, user_of_profile)
    else:
        observer_or_observed_by = None
    
    return observer_or_observed_by