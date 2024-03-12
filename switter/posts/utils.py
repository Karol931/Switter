from .models import Post, Like
from django.contrib.auth.models import User
from django.db.models import Value, IntegerField, Count
from openai import OpenAI
from django.conf import settings
from django.db import connection

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


def get_profile_page_posts(user_of_profile, logged_in_user, sort_method):
    order_method = get_order_method(sort_method)
    with connection.cursor() as cursor:
        query = f""" SELECT p.*, COUNT(l.id) AS like_count, l.user_id
                    FROM posts_Post AS p LEFT JOIN posts_Like AS l ON p.id = l.post_id
                    WHERE p.user_id = {user_of_profile.id}
                        GROUP BY p.id
                        ORDER BY {order_method} DESC;"""
        cursor.execute(query)
        tuple_posts = cursor.fetchall()

        posts = translate_tuple_to_dict(tuple_posts, logged_in_user)

    return posts


def get_main_page_posts(logged_in_user, sort_method):
    order_method = get_order_method(sort_method)

    with connection.cursor() as cursor:
        query = f""" SELECT p.*, COUNT(l.id) AS like_count, l.user_id
                    FROM posts_Post AS p LEFT JOIN posts_Like AS l ON p.id = l.post_id
                    WHERE p.user_id != {logged_in_user.id}
                        GROUP BY p.id
                        ORDER BY {order_method} DESC;"""
        cursor.execute(query)
        tuple_posts = cursor.fetchall()
    
    posts = translate_tuple_to_dict(tuple_posts, logged_in_user)

    return posts

def check_sort_method(session):
    if session.__contains__('sort_method'):
        sort_method = session['sort_method']
    else:
        sort_method = 'newest'
        session['sort_method'] = sort_method
    
    return sort_method


def get_order_method(sort_method):
    if sort_method == 'newest':
        order_method = 'p.date_time'
    elif sort_method == 'most-popular':
        order_method = 'like_count'
    
    return order_method


def translate_tuple_to_dict(tuple_posts, logged_id_user):
    posts = [
        {
            'post_id' : post[0],
            'text' : post[1],
            'date_time' : post[2],
            'user' : User.objects.get(id=post[3]).username,
            'like_number': post[4],
            'is_liked': is_post_liked_by_user(post[0], logged_id_user.id)
        } 
        for post in tuple_posts]
    
    return posts


def is_post_liked_by_user(post_id, user_id):
    likes = Like.objects.filter(post=post_id).values('user')
    for like in likes:
        if like['user'] == user_id:
            return True
    
    return False