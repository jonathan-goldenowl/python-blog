import random
import os

from django_seed import Seed
from blog.models import Category, Article, Author
from django.contrib.auth import get_user_model

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.files import File
from knowledgeshare.settings import BASE_DIR

User = get_user_model()
seeder = Seed.seeder()

images = os.listdir('assets/images')[1:]
@receiver(pre_save, sender=Article)
def cover_image_handler(sender, instance, **kwargs):
  filename = random.choice(images)
  file_content = File(open(BASE_DIR / 'assets' / 'images' / filename, 'rb'))

  instance.cover_image.save(filename, file_content, save=False)

@receiver(post_save, sender=User)
def user_handler(sender, instance, created, **kwargs):
  if created:
    Author.objects.create(
      user=instance,
      bio=seeder.faker.text(),
      pseudonym=seeder.faker.name()
    )

seeder.add_entity(Category, 5, {
  'title': lambda x: seeder.faker.text(max_nb_chars=20)[:-1],
  'description': lambda x: seeder.faker.text(max_nb_chars=200),
  'status': Category.ACTIVE,
})

seeder.add_entity(User, 5, {
  'username': lambda x: seeder.faker.user_name(),
  'first_name': lambda x: seeder.faker.first_name(),
  'last_name': lambda x: seeder.faker.last_name(),
  'email': lambda x: seeder.faker.email(),
  'is_active': True,
  'password': '12345678',
})

seeder.add_entity(Article, 100, {
  'title': lambda x: seeder.faker.text(max_nb_chars=50)[:-1],
  'description': lambda x: seeder.faker.text(max_nb_chars=200),
  'content': lambda x: seeder.faker.text(max_nb_chars=5000),
  'status': Article.PUBLISHED,
  'category': lambda x: random.choice(Category.objects.filter(status=Category.ACTIVE)),
  'author': lambda x: random.choice(Author.objects.all())
})


inserted_pks = seeder.execute()
