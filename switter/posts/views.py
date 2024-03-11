from django.shortcuts import redirect
from .models import Post, Like
from datetime import datetime
from django.contrib import messages
from .utils import check_post_sentiment
# Create your views here.

def add_post(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            new_post = request.POST['new-post']
            if check_post_sentiment(new_post) == 'positive':
                user = request.user
                date_time = datetime.now()
                Post.objects.create(user=user, post=new_post, date_time=date_time)
                messages.success(request, 'Tweet added succesfully.')
            else:
                messages.error(request, 'Tweet didn\'t match our standards.')
        
        return redirect(request.session['current_page'])
   

def delete_post(request):
    if request.method == "POST":
        post_id = request.POST['post-id']
        Post.objects.get(id=post_id).delete()
    
        return redirect(request.session['current_page'])

def add_like(request):
    if request.method == "POST":
        user = request.user
        post_id = request.POST['post-id']
        post = Post.objects.get(id=post_id)
        Like.objects.create(user=user, post=post)
    
        return redirect(request.session['current_page'])

def delete_like(request):
    if request.method == "POST":
        user = request.user
        post_id = request.POST['post-id']
        post = Post.objects.get(id=post_id)
        Like.objects.get(post=post, user=user).delete()
    
        return redirect(request.session['current_page'])

def set_sort_method(request):
    if request.method == "POST":
        request.session['sort_method'] = request.POST['sort-method']
    
        return redirect(request.session['current_page'])