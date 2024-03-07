from . import views
from django.urls import path

urlpatterns = [
    path('add_post/', views.add_post, name='add_post'),
    path('delete_post/', views.delete_post, name='delete_post'),
    path('add_like', views.add_like, name='add_like'),
    path('delete_like', views.delete_like, name='delete_like')
]
