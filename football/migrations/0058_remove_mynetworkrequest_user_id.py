# Generated by Django 4.2.4 on 2023-10-04 13:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0057_alter_mynetworkrequest_from_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mynetworkrequest',
            name='user_id',
        ),
    ]
