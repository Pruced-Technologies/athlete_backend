# Generated by Django 4.2.4 on 2023-10-18 04:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0081_rename_footballcoach_footballcoachinfo'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FootballCoachInfo',
            new_name='FootballCoach',
        ),
    ]
