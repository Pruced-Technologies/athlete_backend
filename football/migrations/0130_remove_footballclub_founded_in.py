# Generated by Django 4.2.4 on 2024-01-19 02:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0129_profiledescription_profile_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='footballclub',
            name='founded_in',
        ),
    ]
