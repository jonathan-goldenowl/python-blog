from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


User = get_user_model()


def user_fullname(self):
    return "{0} {1}".format(self.first_name, self.last_name)


User.add_to_class('fullname', user_fullname)


def get_avatar_upload_path(instance, filename):
    user = instance.user
    return 'uploads/user/{0}/{1}'.format(user.id, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', related_query_name='profile')
    bio = models.CharField(max_length=255, blank=True)
    avatar = models.ImageField(upload_to=get_avatar_upload_path, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.user.username)

    def get_profile_url(self):
        return reverse('users:user_profile', slug=self.user.username)

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return '/assets/images/default-avatar.jpeg'
