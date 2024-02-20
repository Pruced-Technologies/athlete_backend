# Generated by Django 4.2.4 on 2024-02-20 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0135_customuser_is_open_for_hiring'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_open_for_hiring',
        ),
        migrations.AddField(
            model_name='player',
            name='is_open_for_hiring',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='player',
            name='my_worth',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
