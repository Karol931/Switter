from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_observer, name='add_observer'),
    path('delete/', views.delete_observer, name='delete_observer')
]