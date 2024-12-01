from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect

def allowed_users(message, redirect_link, allowed_user_types=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            # get user profile and user type
            if hasattr(request.user, 'profile'):
                user_type = request.user.profile.user_type
                if user_type in allowed_user_types:
                    return view_func(request, *args, **kwargs)
                
            # if user not in allowed user type
            messages.error(request, message)
            return redirect(redirect_link)
        return wrapper_func
    return decorator
