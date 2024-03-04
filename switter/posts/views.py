from django.shortcuts import render, redirect
from .models import Post
from datetime import datetime
from openai import OpenAI
from django.conf import settings
from django.contrib import messages
# Create your views here.

def add_post(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            new_post = request.POST['new-post']
            if check_post_sentiment(new_post) == 'positive':
                user = request.user
                date_time = datetime.now()
                post = Post.objects.create(user=user, post=new_post, date_time=date_time)
                messages.success(request, 'Tweet added succesfully.')
            else:
                messages.error(request, 'Tweet didn\'t match our standards.')
        return redirect('main_page')
    
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