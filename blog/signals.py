from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify

from . import models

def slug_handler(sender, instance, **kwargs):
  if not instance.id:
    instance.slug = slugify(instance.title)

pre_save.connect(slug_handler, sender=models.Category)
pre_save.connect(slug_handler, sender=models.Article)
