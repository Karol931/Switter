from django.shortcuts import render, redirect
from pages.models import PageState
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect

def search(requset: HttpRequest) -> HttpResponseRedirect:
    """
    Handles user search requests and updates the search phrase in the user's page state.

    This function retrieves the search phrase from the request data, updates the `search_phrase` 
    field in the `PageState` model for the current user, and redirects to the 'search_user' page.

    Args:
        request (HttpRequest): The HTTP request object containing the user and search data.

    Returns:
        HttpResponseRedirect: A redirect response to the 'search_user' page.
    """
    search_phrase = requset.data.get('search')
    print(search_phrase)
    page_state = PageState.objects.get(user=requset.user.id)
    page_state.search_phrase = search_phrase
    page_state.save()
    
    return redirect('search_user')