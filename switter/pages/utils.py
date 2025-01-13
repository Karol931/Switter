from django.shortcuts import redirect
from pages.models import PageState
from observers.utils import get_users_observed_by, get_observers_of_user
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.db.models import QuerySet

def get_redirect_page(user: User) -> HttpResponseRedirect:
    """
    Determines the redirect page for a user based on their saved page state.
    
    Fetches the current page state of the user and redirects them to the appropriate page. 
    Supports redirection to 'main_page' and 'profile_page'.
    
    Args:
        user (User): The user for whom the redirect is determined.

    Returns:
        HttpResponseRedirect: A redirect response to the appropriate page.
    """
    page_state = PageState.objects.get(user=user)

    if page_state.page == 'main_page':
        return redirect('main_page')
    elif page_state.page == 'profile_page':
        return redirect('profile_page', username=page_state.profile)
    # elif page_state.page == 'search_page':
    #     return redirect('search_page')
    

def is_same_profile(username: str, logged_in_user: User) -> bool:
    """
    Checks if the provided username matches the last viewed profile by the logged-in user.
    
    Args:
        username (str): The username to compare.
        logged_in_user (User): The currently logged-in user.

    Returns:
        bool: True if the username matches the last viewed profile, False otherwise.
    """
    old_profile = PageState.objects.get(user=logged_in_user).profile
    if old_profile == username:
        return True
    
    return False


def load_sub_window_data(sub_window: str, user_of_profile: User, logged_in_user: User) -> QuerySet[User] | None:
    """
    Loads data for a specific sub-window in a profile view.
    
    Depending on the sub-window type, fetches the appropriate data for either:
    - Users observing the profile owner ('observers')
    - Users observed by the profile owner ('observed_by')
    
    Args:
        sub_window (str): The type of sub-window ('observers' or 'observed_by').
        user_of_profile (User): The user whose profile is being viewed.
        logged_in_user (User): The currently logged-in user.

    Returns:
        QuerySet or None: A QuerySet of users for the specified sub-window type, or None if the sub-window type is invalid.
    """
    if sub_window == 'observers':
        observer_or_observed_by = get_observers_of_user(logged_in_user, user_of_profile)
    elif sub_window == 'observed_by':
        observer_or_observed_by = get_users_observed_by(logged_in_user, user_of_profile)
    else:
        observer_or_observed_by = None
    
    return observer_or_observed_by