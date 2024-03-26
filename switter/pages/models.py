from django.db import models
from django.contrib.auth.models import User


class PageState(models.Model):
    user = models.OneToOneField(to=User, to_field='id', on_delete=models.CASCADE, default=None)
    page = models.CharField(max_length=255, default='main_page')
    profile = models.CharField(max_length=255, default=None, null=True)
    sub_window = models.CharField(max_length=255, default=None, null=True)
    sort_method = models.CharField(max_length=255, default='newest')