from django import forms
# from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
  username = forms.CharField(
    label='Username',
    max_length=255,
    required=True,
    widget=forms.TextInput(attrs={'placeholder': 'Enter your username'})
  )
  password = forms.CharField(
    label='Password',
    max_length=255,
    required=True,
    widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'})
  )

class UserRegisterForm(UserCreationForm):
  email = forms.EmailField()

  class Meta:
    model = User
    fields = ('username', 'email', 'password1', 'password2')
