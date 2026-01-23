from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def sub_admin_required(function=None):
    """
    Decorator for views that checks that the user is a Samaj Admin or Sub-Admin.
    """
    def check_sub_admin(user):
        if not user.is_authenticated:
            return False
        if user.is_samaj_admin():
            return True
        raise PermissionDenied("You do not have permission to access this page.")
        
    actual_decorator = user_passes_test(check_sub_admin)
    if function:
        return actual_decorator(function)
    return actual_decorator

def main_admin_required(function=None):
    """
    Decorator for views that checks that the user is the Main Admin.
    """
    def check_main_admin(user):
        if not user.is_authenticated:
            return False
        if user.is_main_admin():
            return True
        raise PermissionDenied("Only Main Admins can access this page.")
        
    actual_decorator = user_passes_test(check_main_admin)
    if function:
        return actual_decorator(function)
    return actual_decorator
