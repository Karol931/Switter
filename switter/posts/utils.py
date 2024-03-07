from .models import Post, Like
from django.contrib.auth.models import User
from openai import OpenAI
from django.conf import settings

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


def get_logged_in_user_posts(logged_in_user):
    posts = Post.objects.filter(user=logged_in_user).order_by('-date_time')

    return posts

def get_main_page_posts(logged_in_user):
    posts = Post.objects.exclude(user=logged_in_user).order_by('-date_time')
    user = User.objects.get(id=logged_in_user.id)
    print(user.id)
    like_numbers = [get_like_number(post) for post in posts]
    
    is_post_liked_by_user_list = are_posts_liked_by_user(posts, logged_in_user)
    
    for post, like_number, is_liked in zip(posts, like_numbers, is_post_liked_by_user_list):
        post.like_number = like_number
        post.is_liked = is_liked

    return posts

def get_like_number(post):
    
    return Like.objects.filter(post=post).count()

def are_posts_liked_by_user(posts, user):
    is_post_liked_by_user_list = []
    counter = 0
    for post in posts:
        likes = Like.objects.filter(post=post).values('user')
        for like in likes:
            if like['user'] == user.id:
                is_post_liked_by_user_list.append(True)
        if len(is_post_liked_by_user_list) -1 < counter:
            is_post_liked_by_user_list.append(False)
        counter += 1
    
    return is_post_liked_by_user_list