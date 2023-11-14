# Generated by Django 4.2.4 on 2023-10-06 16:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0062_networkconnected'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='networkconnected',
            name='user_id',
        ),
        migrations.AlterField(
            model_name='networkconnected',
            name='connected_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='connected_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
