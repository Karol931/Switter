from django.contrib.auth.models import User
from .models import Observer
from django.db.models import ExpressionWrapper, Q, BooleanField, Count

def get_users_to_observe(logged_in_user):
    observers = Observer.objects.filter(observed_by=logged_in_user)
    observers_ids = list(observers.values_list('observer', flat=True))
    observers_ids.append(logged_in_user.id)
    users_to_observe = User.objects.exclude(id__in=observers_ids).order_by('username')

    return users_to_observe

def get_observer_of_count(user):
    observer_of_count = Observer.objects.filter(observed_by=user).count()

    return observer_of_count

def get_observed_by_count(user):
    observed_by_user_count = Observer.objects.filter(observer=user).count()

    return observed_by_user_count

def get_users_observed_by(logged_in_user, user):
    observed_by_logged_in_user = [observer['observer'] for observer in Observer.objects.filter(observed_by=logged_in_user).values('observer')]
    print(observed_by_logged_in_user)
    observed_by_user_ids = Observer.objects.filter(observer=user).values('observed_by')
    
    observed_by_user = User.objects.filter(id__in=observed_by_user_ids).annotate(is_observed_by_logged_in_user=ExpressionWrapper(Q(id__in=observed_by_logged_in_user), output_field=BooleanField()))
    print(observed_by_user.values())

    return observed_by_user

def get_observers_of_user(logged_in_user, user):
    observed_by_logged_in_user_ids = [observer['observer'] for observer in Observer.objects.filter(observed_by=logged_in_user).values('observer')]
    print(observed_by_logged_in_user_ids)

    observres_of_user_ids = Observer.objects.filter(observed_by=user).values('observer')
    
    observres_of_user = User.objects.filter(id__in=observres_of_user_ids).annotate(is_observed_by_logged_in_user=ExpressionWrapper(Q(id__in=observed_by_logged_in_user_ids), output_field=BooleanField()))
    
    print(observres_of_user.values())
    return observres_of_user