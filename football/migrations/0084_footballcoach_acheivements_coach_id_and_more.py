# Generated by Django 4.2.4 on 2023-10-18 04:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0083_remove_acheivements_coach_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FootballCoach',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('from_date', models.IntegerField(blank=True, null=True)),
                ('to_date', models.IntegerField(blank=True, null=True)),
                ('playoffs_games_coached_in', models.IntegerField(blank=True, null=True)),
                ('playoffs_games_won', models.IntegerField(blank=True, null=True)),
                ('playoffs_games_lost', models.IntegerField(blank=True, null=True)),
                ('total_no_tournaments_won_as_coach', models.IntegerField(blank=True, null=True)),
                ('current_team', models.TextField(blank=True, null=True)),
                ('current_club_inside', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='coach_club', to='football.footballclub')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='coach', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='acheivements',
            name='coach_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='coach_acheivements', to='football.footballcoach'),
        ),
        migrations.AddField(
            model_name='footballcoachcareerhistory',
            name='coach_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='carreer_history', to='football.footballcoach'),
        ),
        migrations.AddField(
            model_name='footballtournaments',
            name='coach_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tournaments_name_won_as_coach', to='football.footballcoach'),
        ),
    ]
