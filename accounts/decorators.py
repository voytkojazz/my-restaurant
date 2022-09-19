from django.shortcuts import redirect
from django.contrib import messages

def unautheticated_user(view_function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, ('You are already register. In order to register, please, sign out'))
            return redirect('home')
        else:
            return view_function(request, *args, **kwargs)
    return wrapper


def not_unautheticated_user(view_function):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.success(request, ('In order to proceed further, you must to log in first...'))
            return redirect('login-page')
        else:
            return view_function(request, *args, **kwargs)
    return wrapper


    