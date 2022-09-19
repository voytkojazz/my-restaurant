from django.urls import path

from . import views

urlpatterns = [
    path('login-me/', views.login_user, name='login-page'),
    path('logout-me/', views.logout_user, name='logout-page'),
    path('register-me/', views.register_user, name='register-page'),
]

