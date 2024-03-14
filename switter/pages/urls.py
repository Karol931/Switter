from . import views
from django.urls import path

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('profile/<str:username>', views.profile_page, name='profile_page'),
]
