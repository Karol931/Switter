from django.contrib.auth.models import User
from .models import Observer

def get_users_observers(logged_in_user):
    observers = Observer.objects.filter(observed_by=logged_in_user.id)
    observers_ids = observers.values_list('observer', flat=True)
    observers = User.objects.filter(id__in=observers_ids).order_by('username')
    return observers

def get_users_to_observe(loged_in_user):
    observers = Observer.objects.filter(observed_by=loged_in_user)
    observers_ids = list(observers.values_list('observer', flat=True))
    observers_ids.append(loged_in_user.id)
    users_to_observe = User.objects.exclude(id__in=observers_ids).order_by('username')
    return users_to_observe