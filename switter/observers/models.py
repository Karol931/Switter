from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Observer(models.Model):
    observer = models.ForeignKey(to=User, to_field='id', on_delete=models.CASCADE, default=None, related_name='observer')
    observed_by = models.ForeignKey(to=User, to_field='id', on_delete=models.CASCADE, default=None, related_name='observed_by')