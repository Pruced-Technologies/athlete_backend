# Generated by Django 4.2.4 on 2023-12-31 04:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0120_alter_postcomments_options_news'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='user',
        ),
        migrations.AddField(
            model_name='news',
            name='user',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
