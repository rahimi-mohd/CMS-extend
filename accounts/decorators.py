from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect

def allowed_users(message, redirect_link, allowed_groups=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.groups.exists():
                user_groups = request.user.groups.values_list('name', flat=True)

                if any(group in allowed_groups for group in user_groups):
                    return view_func(request, *args, **kwargs)
                
            # if user not in allowed group
            messages.error(request, message)
            return redirect(redirect_link)
        return wrapper_func
    return decorator
