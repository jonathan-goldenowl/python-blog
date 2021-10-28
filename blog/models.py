import uuid
from django.db import models
from django.conf import settings
from django.utils.html import mark_safe
from django.contrib.auth import get_user_model

User = get_user_model()

def get_upload_path(instance, filename):
  return 'uploads/blog/{0}/{1}/{2}'.format(
    instance.__class__._meta.model_name,
    instance.uuid,
    filename
  )

class Author(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  bio = models.TextField()
  pseudonym = models.CharField(max_length=100, default=user.name)

  def __str__(self):
    return self.pseudonym or self.user.name

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
  featured = models.BooleanField(default=False, null=False)

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
  uuid = models.UUIDField(null=False, default=uuid.uuid4, editable=False)
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
  featured = models.BooleanField(default=False, null=False)

  def cover_image_tag(self):
    return mark_safe('<img src="/%s" width="150" height="150" style="object-fit: scale-down">' % self.cover_image)

  def is_status(self, status):
    return self.status == status

  def __str__(self):
    return self.title
