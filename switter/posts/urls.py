from . import views
from django.urls import path

urlpatterns = [
    path('add_post/', views.add_post, name='add_post'),
]