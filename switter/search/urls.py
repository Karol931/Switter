from django.contrib import admin
from django.urls import path
from . import views
from pages.views import search_page

urlpatterns = [
    path('users/', views.users, name='search_user'),
    path('posts/', views.posts, name='search_post'),
    path('', search_page, name='search_page'),
]