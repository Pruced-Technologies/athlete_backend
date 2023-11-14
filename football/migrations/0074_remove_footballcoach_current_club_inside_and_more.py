# Generated by Django 4.2.4 on 2023-10-18 01:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0073_remove_footballcoach_current_club_inside_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='footballcoach',
            name='current_club_inside',
        ),
        migrations.RemoveField(
            model_name='player',
            name='current_club_inside',
        ),
        migrations.AddField(
            model_name='footballcoach',
            name='current_club_inside',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='coach_club', to='football.footballclub'),
        ),
        migrations.AddField(
            model_name='player',
            name='current_club_inside',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player_club', to='football.footballclub'),
        ),
    ]
