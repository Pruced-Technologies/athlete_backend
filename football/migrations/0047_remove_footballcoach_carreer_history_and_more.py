# Generated by Django 4.2.4 on 2023-09-09 15:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0046_remove_playervideoclip_user_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='footballcoach',
            name='carreer_history',
        ),
        migrations.RemoveField(
            model_name='footballcoach',
            name='player',
        ),
        migrations.RemoveField(
            model_name='footballcoach',
            name='tournaments_name_won_as_coach',
        ),
        migrations.RemoveField(
            model_name='footballcoachcareerhistory',
            name='tournaments_name_won_as_player',
        ),
        migrations.AddField(
            model_name='footballcoachcareerhistory',
            name='coach_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='carreer_history', to='football.footballcoach'),
        ),
        migrations.AddField(
            model_name='footballtournaments',
            name='tournaments_won_as_coach',
            field=models.ManyToManyField(blank=True, related_name='tournaments_name_won_as_coach', to='football.footballcoach'),
        ),
        migrations.AddField(
            model_name='footballtournaments',
            name='tournaments_won_as_player',
            field=models.ManyToManyField(blank=True, related_name='tournaments_name_won_as_player', to='football.footballcoachcareerhistory'),
        ),
        migrations.AlterField(
            model_name='footballcoach',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='coach', to=settings.AUTH_USER_MODEL),
        ),
    ]
