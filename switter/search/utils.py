from django.shortcuts import render, redirect
from pages.models import PageState
from django.http import HttpResponse

def search(requset):
    search_phrase = requset.data.get('search')
    print(search_phrase)
    page_state = PageState.objects.get(user=requset.user.id)
    page_state.search_phrase = search_phrase
    page_state.save()
    
    return redirect('search_user')