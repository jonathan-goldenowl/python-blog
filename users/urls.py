from django.contrib.auth import logout
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
  path('login', views.login, name='login'),
  path('logout', views.logout, name='logout'),
  path('register', views.register, name='register'),
  path('edit_profile', views.edit_profile, name='edit_profile'),
]