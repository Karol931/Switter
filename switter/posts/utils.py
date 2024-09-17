from .models import Like
from django.contrib.auth.models import User
from pages.models import PageState
from openai import OpenAI
from django.conf import settings
from posts.models import Post
from django.db.models import Count, F


def check_post_sentiment(post_text):
    API_KEY = setattr(settings, 'OPENAI_API_KEY', None)
    client = OpenAI(api_key=API_KEY)
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'system', 'content': 'You are a person who makes sentiment analysis of text, anwser with one of the folowing words: positive, neutral, negative.'},
            {'role': 'user', 'content': post_text}
        ]
    )

    return response.choices[0].message.content


def get_profile_page_posts(user_of_profile, logged_in_user):

    posts = Post.objects.filter(user=user_of_profile).values()
    
    posts = [
        {
            'post_id' : post['id'],
            'text' : post['post'],
            'date_time' : post['date_time'],
            'user' : User.objects.get(id=post['user_id']).username,
            'like_number': get_post_likes(post),
            'is_liked': is_post_liked_by_user(post['id'], logged_in_user.id)
        } 
        for post in posts]
    
    posts = sort_posts(logged_in_user, posts)

    return posts

def get_main_page_posts(logged_in_user):

    posts = Post.objects.exclude(user=logged_in_user).values()
    
    posts = [
        {
            'post_id' : post['id'],
            'text' : post['post'],
            'date_time' : post['date_time'],
            'user' : User.objects.get(id=post['user_id']).username,
            'like_number': get_post_likes(post),
            'is_liked': is_post_liked_by_user(post['id'], logged_in_user.id)
        } 
        for post in posts]
    
    posts = sort_posts(logged_in_user, posts)

    return posts


def check_sort_method(user):
    sort_method = PageState.objects.get(user=user).sort_method
    
    return sort_method


def sort_posts(user, posts):
    sort_method = check_sort_method(user)
    if sort_method == 'newest':
        order_method = 'date_time'
    elif sort_method == 'most-popular':
        order_method = 'like_number'
    posts = sorted(posts, key=lambda x:x[order_method], reverse=True if order_method=='like_number' else False)
    return posts


def get_post_likes(post):
    like_number = Like.objects.filter(post=post['id']).count()

    return like_number


def is_post_liked_by_user(post_id, user_id):
    likes = Like.objects.filter(post=post_id).values('user')
    for like in likes:
        if like['user'] == user_id:
            return True
    
    return False