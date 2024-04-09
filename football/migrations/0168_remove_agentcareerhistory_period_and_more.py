# Generated by Django 4.2.4 on 2024-04-08 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0167_remove_club_period_club_from_year_club_to_year'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agentcareerhistory',
            name='period',
        ),
        migrations.RemoveField(
            model_name='footballcoachcareerhistory',
            name='period',
        ),
        migrations.AddField(
            model_name='agentcareerhistory',
            name='from_year',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='agentcareerhistory',
            name='to_year',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='footballcoachcareerhistory',
            name='from_year',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='footballcoachcareerhistory',
            name='to_year',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
