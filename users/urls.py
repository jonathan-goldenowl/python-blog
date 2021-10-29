from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

app_name = 'users'

urlpatterns = [
  path('login/', views.login, name='login'),
  path('logout/', views.logout, name='logout'),
  path('register/', views.register, name='register'),
  path('edit_profile/', views.edit_profile, name='edit_profile'),
  path('password_change/',
    auth_views.PasswordChangeView.as_view(
      success_url=reverse_lazy('users:password_change_done'),
      template_name='users/password/password_change_form.html',
    ),
    name='password_change'),
  path("password_change/done", views.password_changed, name='password_change_done'),
  path("password_reset/", views.password_reset_request, name='password_reset'),
  path('password_reset/done/',
    auth_views.PasswordResetDoneView.as_view(template_name='users/password/password_reset_done.html'),
    name='password_reset_done'),
  path('reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(
      success_url=reverse_lazy('users:password_reset_complete'),
      template_name="users/password/password_reset_confirm.html"
    ),
    name='password_reset_confirm'),
  path('reset/done/',
    auth_views.PasswordResetCompleteView.as_view(template_name='users/password/password_reset_complete.html'),
    name='password_reset_complete'),
  path('my_profile/', views.UserProfile.as_view(), name='my_profile'),
  path('<slug:slug>/profile/', views.UserProfile.as_view(), name='user_profile')
]
