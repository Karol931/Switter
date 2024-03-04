from django.shortcuts import render
from django.contrib.auth.models import User
from posts.models import Post
from openai import OpenAI
# Create your views here.

def main_page(request):
    if request.user.is_authenticated:
        username =request.user
        posts = get_posts()
        return render(request, 'main_page.html', {'username' : username, 'posts': posts})
    
def get_posts():
    posts = Post.objects.all().order_by('-date_time')
    return posts

def check_post_sentiment(post_text):
    client = OpenAI()
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        message=[
            {'role': 'system', 'content': 'You are a person who makes sentiment analysis of text, anwser with one of the folowing words: positive, neutral, negative.'},
            {'role': 'user',
             'content': post_text}
        ]
    )
    print(response.choises[0].message)