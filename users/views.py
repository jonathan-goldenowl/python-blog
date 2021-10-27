from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib import messages
from django.urls import reverse


from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.http import HttpResponse
from django.conf import settings


from .models import Profile
from .forms import LoginForm, UserRegisterForm, UserUpdateForm, ProfileUpdateform


User = get_user_model()

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

def password_reset_request(request):
  if request.user.is_authenticated:
    messages.info(request, 'Your are already logged in!')
    return redirect(reverse('root'))

  if request.method == 'POST':
    password_reset_form = PasswordResetForm(request.POST)

    if password_reset_form.is_valid():
      email = password_reset_form.cleaned_data['email']
      associated_users = User.objects.filter(email=email)

      if associated_users.exists():
        for user in associated_users:
          subject = "Password Reset Requested"
          email_template_name = "users/password/password_reset_email.txt"
          data = {
            "email": user.email,
            'domain': '127.0.0.1:8000',
            'site_name': 'Website',
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "user": user,
            'token': default_token_generator.make_token(user),
            'protocol': 'http',
          }
          template = render_to_string(email_template_name, data)
          try:
            send_mail(subject, template, settings.EMAIL_SENDER , [user.email], fail_silently=False)
          except BadHeaderError:
            return HttpResponse('Invalid header found.')
          return redirect ("/password_reset/done/")
      else:
        messages.error(request, f'Email not found!')
  password_reset_form = PasswordResetForm()
  context = { 'password_reset_form' : password_reset_form }

  return render(request, 'users/password/password_reset.html', context)

@login_required
def password_changed(request):
  messages.success(request, 'Your password has been changed.')
  return redirect(request.POST.get('next', reverse('users:edit_profile')))
