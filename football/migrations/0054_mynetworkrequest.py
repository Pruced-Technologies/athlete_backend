# Generated by Django 4.2.4 on 2023-09-26 02:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0053_customuser_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyNetworkRequest',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fromUser', models.CharField(max_length=100)),
                ('toUser', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_network', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
