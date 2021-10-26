from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from .models import Profile
from .forms import LoginForm, UserRegisterForm, UserUpdateForm, ProfileUpdateform


def register(request):
  if request.user.is_authenticated:
    messages.error(request, f'Your are already logged in!')
    return redirect('/')

  if request.method == 'GET':
    form = UserRegisterForm()
  elif request.method == 'POST':
    form = UserRegisterForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, f'Your account has been created! You can now login!')
      return redirect(reverse('users:login'))

  return render(request, 'users/register.html', { 'register_form': form })

def login(request):
  if request.method == 'GET':
    form = LoginForm()
  elif request.method == 'POST':
    user = authenticate(
      username=request.POST['username'],
      password=request.POST['password']
    )

    if user is not None:
      auth_login(request, user)
      return redirect('/')
    else:
      messages.error(request, "Invalid username or password")
      form = LoginForm()

  return render(request, 'users/login.html', { 'login_form': form })

@login_required
def logout(request):
  auth_logout(request)
  messages.success(request, "You are logged out!")

  return redirect('/')

@login_required
def edit_profile(request):
  user = request.user
  profile, created = Profile.objects.get_or_create(user=user)

  if request.method == 'POST':
    user_form = UserUpdateForm(request.POST, instance=user)
    profile_form = ProfileUpdateform(request.POST, request.FILES, instance=profile)

    if user_form.is_valid() and profile_form.is_valid():
      user_form.save()
      profile_form.save()
      messages.success(request, f'Your account has been updated!')
      return redirect(reverse('root'))
  else:
    user_form = UserUpdateForm(instance=user)
    profile_form = ProfileUpdateform(instance=profile)

  context = {
    'user_form': user_form,
    'profile_form': profile_form,
  }

  return render(request, 'users/edit_profile.html', context)