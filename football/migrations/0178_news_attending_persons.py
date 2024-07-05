# Generated by Django 4.2.4 on 2024-05-30 16:12

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0177_postitem_post_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='attending_persons',
            field=models.ManyToManyField(blank=True, related_name='attending_persons', to=settings.AUTH_USER_MODEL),
        ),
    ]
