# Generated by Django 4.2.4 on 2023-11-22 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0110_player_current_club_inside_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='footballcoach',
            name='current_team',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
