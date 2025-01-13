from .models import Like
from django.contrib.auth.models import User
from pages.models import PageState
from openai import OpenAI
from django.conf import settings
from posts.models import Post
from django.db.models import Count, F
from typing import List, Dict, Any


def check_post_sentiment(post_text: str) -> str:
    """
    Analyzes the sentiment of a given text using an external OpenAI API.

    Args:
        post_text (str): The text of the post to analyze.

    Returns:
        str: The sentiment of the text. One of: 'positive', 'neutral', 'negative'.
    """
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


def get_profile_page_posts(user_of_profile: User, logged_in_user: User) -> List[Dict[str, Any]]:
    """
    Retrieves and formats posts for a user's profile page.

    Args:
        user_of_profile (User): The user whose profile posts are being retrieved.
        logged_in_user (User): The currently logged-in user.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing post data, sorted according to the logged-in user's preferences.
    """
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

def get_main_page_posts(logged_in_user: User) -> List[Dict[str, Any]]:
    """
    Retrieves and formats posts for the main page, excluding the logged-in user's posts.

    Args:
        logged_in_user (User): The currently logged-in user.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing post data, sorted according to the logged-in user's preferences.
    """
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


def check_sort_method(user: User) -> str:
    """
    Retrieves the sorting method preference for a given user.

    Args:
        user (User): The user whose sort method is being retrieved.

    Returns:
        str: The sorting method, such as 'newest' or 'most-popular'.
    """
    sort_method = PageState.objects.get(user=user).sort_method
    
    return sort_method


def sort_posts(user: User, posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Sorts posts based on the user's preferred sorting method.

    Args:
        user (User): The user whose sort preferences are being used.
        posts (List[Dict[str, Any]]): A list of post dictionaries to be sorted.

    Returns:
        List[Dict[str, Any]]: The sorted list of posts.
    """
    sort_method = check_sort_method(user)
    if sort_method == 'newest':
        order_method = 'date_time'
    elif sort_method == 'most-popular':
        order_method = 'like_number'
    posts = sorted(posts, key=lambda x:x[order_method], reverse=True if order_method=='like_number' else False)
    return posts


def get_post_likes(post: Post) -> int:
    """
    Retrieves the number of likes for a given post.

    Args:
        post (Dict[str, Any]): A dictionary containing post data.

    Returns:
        int: The number of likes for the post.
    """
    like_number = Like.objects.filter(post=post['id']).count()

    return like_number


def is_post_liked_by_user(post_id: int, user_id: int) -> bool:
    """
    Checks if a specific post is liked by a specific user.

    Args:
        post_id (int): The ID of the post.
        user_id (int): The ID of the user.

    Returns:
        bool: True if the user has liked the post, False otherwise.
    """
    likes = Like.objects.filter(post=post_id).values('user')
    for like in likes:
        if like['user'] == user_id:
            return True
    
    return False