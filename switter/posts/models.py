from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(to=User, to_field='id', on_delete=models.CASCADE, default=None)
    post = models.TextField(max_length=255)
    date_time = models.DateTimeField()

class Like(models.Model):
    user = models.ForeignKey(to=User, to_field='id', on_delete=models.CASCADE, default=None)
    post = models.ForeignKey(to=Post, to_field='id', on_delete=models.CASCADE, default=None)