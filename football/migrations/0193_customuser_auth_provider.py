# Generated by Django 4.2.4 on 2024-07-03 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0192_customuser_reg_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='auth_provider',
            field=models.CharField(default='email', max_length=50),
        ),
    ]
