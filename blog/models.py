from django.db import models
from django.conf import settings

from django.contrib.auth import get_user_model

User = get_user_model()

def get_upload_path(instance, filename):
  return '{0}/blog/{1}/{2}/{3}'.format(
    settings.UPLOAD_ROOT,
    instance.__class__._meta.model_name,
    instance.id,
    filename
  )

class Author(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  bio = models.TextField()
  pseudonym = models.CharField(max_length=100, default=user.name)

class Category(models.Model):
  ACTIVE = 'active'
  INACTIVE = 'inactive'
  STATUS_CHOICES = [
    (ACTIVE, 'Active'),
    (INACTIVE, 'Inactive')
  ]

  # fields
  title = models.CharField(max_length=100)
  description = models.CharField(max_length=255)
  status = models.CharField(
    max_length=30,
    choices=STATUS_CHOICES,
    default=ACTIVE
  )
  slug = models.SlugField(max_length=255, blank=True)

  def __str__(self):
    return self.title

class Article(models.Model):
  DRAFT = 'draft'
  PENDING = 'pending'
  PUBLISHED = 'published'
  REJECTED = 'rejected'
  BLOCKED = 'blocked'
  STATUSES_CHOICES = [
    (DRAFT, 'Draft'),
    (PUBLISHED, 'Published'),
    (PENDING, 'Waiting for Review'),
    (REJECTED, 'Rejected'),
    (BLOCKED, 'Blocked')
  ]

  # fields
  title = models.CharField(max_length=255)
  description = models.CharField(max_length=255)
  content = models.TextField()
  cover_image = models.ImageField(upload_to=get_upload_path)
  status = models.CharField(
    max_length=30,
    choices=STATUSES_CHOICES,
    default=DRAFT
  )
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  # associations
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  author = models.ForeignKey(Author, on_delete=models.CASCADE)
  slug = models.SlugField(max_length=255, blank=True)
  num_views = models.PositiveIntegerField('Number of views', default=0)

  def is_status(self, status):
    return self.status == status

  def __str__(self):
    return self.title
