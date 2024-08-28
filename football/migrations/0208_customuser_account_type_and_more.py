# Generated by Django 4.2.4 on 2024-08-17 15:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0207_alter_address_permanent_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='account_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='permanent_user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='permanent_address', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='sportprofiletype',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sport_profile_type', to=settings.AUTH_USER_MODEL),
        ),
    ]
