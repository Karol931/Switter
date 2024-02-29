from django.shortcuts import render, redirect
from .models import Post
from datetime import datetime
# Create your views here.

def add_post(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            new_post = request.POST['new-post']
            user = request.user
            date_time = datetime.now()
            post = Post.objects.create(user=user, post=new_post, date_time=date_time)
        return redirect('main_page')