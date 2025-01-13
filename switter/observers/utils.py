from django.contrib.auth.models import User
from .models import Observer
from django.db.models import ExpressionWrapper, Q, BooleanField, QuerySet


def get_users_to_observe(logged_in_user: User) -> QuerySet[User]:
    """
    Retrieves a list of users that the given user can observe.
    
    Users who are already being observed by the logged-in user or the logged-in user themselves 
    are excluded from the result. The returned list is ordered by username.
    
    Args:
        logged_in_user (User): The currently logged-in user.

    Returns:
        QuerySet: A QuerySet of users available to observe.
    """
    observers = Observer.objects.filter(observed_by=logged_in_user)
    observers_ids = list(observers.values_list('observer', flat=True))
    observers_ids.append(logged_in_user.id)
    users_to_observe = User.objects.exclude(id__in=observers_ids).order_by('username')

    return users_to_observe


def get_observer_of_count(user: User) -> QuerySet[User]:
    """
    Counts the number of users being observed by the given user.
    
    Args:
        user (User): The user whose observed count is being retrieved.

    Returns:
        int: The number of users observed by the user.
    """
    observer_of_count = Observer.objects.filter(observed_by=user).count()

    return observer_of_count


def get_observed_by_count(user: User) -> QuerySet[Observer]:
    """
    Counts the number of users observing the given user.
    
    Args:
        user (User): The user whose observer count is being retrieved.

    Returns:
        int: The number of users observing the user.
    """
    observed_by_user_count = Observer.objects.filter(observer=user).count()

    return observed_by_user_count


def get_users_observed_by(logged_in_user: User, user: User) -> QuerySet[User]:
    """
    Retrieves a list of users observing a specific user and indicates if they are observed by the logged-in user.
    
    Args:
        logged_in_user (User): The currently logged-in user.
        user (User): The user whose observers are being retrieved.

    Returns:
        QuerySet: A QuerySet of users observing the specified user with an additional 
                  `is_observed_by_logged_in_user` annotation indicating if they are observed by the logged-in user.
    """
    observed_by_logged_in_user = [observer['observer'] for observer in Observer.objects.filter(observed_by=logged_in_user).values('observer')]
    print(observed_by_logged_in_user)
    observed_by_user_ids = Observer.objects.filter(observer=user).values('observed_by')
    
    observed_by_user = User.objects.filter(id__in=observed_by_user_ids).annotate(is_observed_by_logged_in_user=ExpressionWrapper(Q(id__in=observed_by_logged_in_user), output_field=BooleanField()))
    print(observed_by_user.values())

    return observed_by_user


def get_observers_of_user(logged_in_user, user: User) -> QuerySet[User]:
    """
    Retrieves a list of users being observed by a specific user and indicates if they are observed by the logged-in user.
    
    Args:
        logged_in_user (User): The currently logged-in user.
        user (User): The user whose observed users are being retrieved.

    Returns:
        QuerySet: A QuerySet of users being observed by the specified user with an additional 
                  `is_observed_by_logged_in_user` annotation indicating if they are observed by the logged-in user.
    """
    observed_by_logged_in_user_ids = [observer['observer'] for observer in Observer.objects.filter(observed_by=logged_in_user).values('observer')]
    print(observed_by_logged_in_user_ids)

    observres_of_user_ids = Observer.objects.filter(observed_by=user).values('observer')
    
    observres_of_user = User.objects.filter(id__in=observres_of_user_ids).annotate(is_observed_by_logged_in_user=ExpressionWrapper(Q(id__in=observed_by_logged_in_user_ids), output_field=BooleanField()))
    
    print(observres_of_user.values())
    return observres_of_user


def is_observed_by_check(logged_in_user: User, user: User) -> bool:
    """
    Checks if a specific user is observed by the logged-in user.
    
    Args:
        logged_in_user (User): The currently logged-in user.
        user (User): The user to check if they are observed by the logged-in user.

    Returns:
        bool: True if the user is observed by the logged-in user, False otherwise.
    """
    is_observed_by = Observer.objects.filter(observed_by = logged_in_user.id, observer = user['id'])
    
    if is_observed_by:
        return True    
    return False
