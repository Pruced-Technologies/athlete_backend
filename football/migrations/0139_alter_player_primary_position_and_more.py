# Generated by Django 4.2.4 on 2024-02-20 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0138_player_current_club'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='primary_position',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='secondary_position',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
