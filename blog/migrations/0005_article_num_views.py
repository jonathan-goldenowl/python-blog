# Generated by Django 3.2.8 on 2021-10-22 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20211021_0811'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='num_views',
            field=models.PositiveIntegerField(default=0, verbose_name='Number of views'),
        ),
    ]
