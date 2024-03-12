from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_observer, name='add_observer'),
    path('delete/', views.delete_observer, name='delete_observer'),
    path('open_observe/', views.open_observe, name='open_observe'),
    path('close_observe/', views.close_observe, name='close_observe'),
    path('open_observed_by/', views.open_observed_by, name='open_observed_by'),
    path('close_observed_by/', views.close_observed_by, name='close_observed_by'),
]