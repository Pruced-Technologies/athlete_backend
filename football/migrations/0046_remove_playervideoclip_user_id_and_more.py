# Generated by Django 4.2.4 on 2023-09-06 13:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0045_acheivements_remove_footballcoach_acheivements_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playervideoclip',
            name='user_id',
        ),
        migrations.AddField(
            model_name='playervideoclip',
            name='user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='video_clip', to=settings.AUTH_USER_MODEL),
        ),
    ]
