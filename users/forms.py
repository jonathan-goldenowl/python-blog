from string import Template
from django.utils.safestring import mark_safe
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Profile


class PictureWidget(forms.widgets.Widget):
  def render(self, name, value, attrs=None, **kwargs):
    html = Template(
      """
        <div style="max-width: 250px">
          <img class="img-thumbnail" src="$link"/>
        </div>
        <br>
        <input type="file" name="$name" />
      """
    )
    return mark_safe(html.substitute(link=value, name=name))

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

class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email')

class ProfileUpdateform(forms.ModelForm):
  date_of_birth = forms.DateField(
    widget=forms.DateInput(
      format=('%m/%d/%Y'),
      attrs={ 'class':'datepicker date_of_birth', 'placeholder':'Select a date' }
    )
  )
  avatar = forms.ImageField(required=False, widget=PictureWidget)
  class Meta:
    model = Profile
    fields = ('date_of_birth', 'bio', 'avatar')
