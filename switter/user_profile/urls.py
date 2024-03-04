from . import views
from django.urls import path

urlpatterns = [
    path('', views.profile_page, name='profile_page'),

]
