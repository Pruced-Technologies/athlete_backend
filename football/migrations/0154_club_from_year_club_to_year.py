# Generated by Django 4.2.4 on 2024-04-12 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0153_remove_club_from_year_remove_club_to_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='from_year',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='club',
            name='to_year',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
