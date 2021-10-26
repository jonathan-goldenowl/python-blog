import uuid
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify

from . import models

def slug_handler(sender, instance, **kwargs):
  if not instance.id:
    instance.slug = slugify(instance.title)
    is_instance_exits = instance.__class__.objects.filter(slug=instance.slug).exists()

    if is_instance_exits:
      instance.slug += '-' + str(uuid.uuid4())

pre_save.connect(slug_handler, sender=models.Category)
pre_save.connect(slug_handler, sender=models.Article)
