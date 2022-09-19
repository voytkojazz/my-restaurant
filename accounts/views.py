from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm
from .decorators import unautheticated_user
# Create your views here.

@unautheticated_user
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ('Now you are loged it!'))
            return redirect('home')
        else:
            messages.success(request, ('There was an error logging in. Try again!'))
            return redirect('login-page')
    else:
        context = {}
        return render(request, 'accounts/login.html', context)


def logout_user(request):
    logout(request)
    messages.success(request, ('You were logged out... '))
    return redirect('home')

@unautheticated_user
def register_user(request): 
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ('Registration successful.'))
            return redirect('home')
    else:
        form = RegisterUserForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/register-me.html', context)