from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

def get_avatar_upload_path(instance, filename):
  user = instance.user
  return 'uploads/user/{0}/{1}'.format(user.id, filename)

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.CharField(max_length=255, blank=True)
	avatar = models.ImageField(upload_to=get_avatar_upload_path, blank=True, null=True)
	date_of_birth = models.DateField(blank=True, null=True)

	def __str__(self):
		return str(self.user.username)

	def get_absolute_url(self):
		return "/users/{}".format(self.user.username)
