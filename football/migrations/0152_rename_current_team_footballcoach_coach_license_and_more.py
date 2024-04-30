# Generated by Django 4.2.4 on 2024-03-26 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0151_alter_league_sport_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='footballcoach',
            old_name='current_team',
            new_name='coach_license',
        ),
        migrations.RenameField(
            model_name='footballcoachcareerhistory',
            old_name='league',
            new_name='country_name',
        ),
        migrations.RenameField(
            model_name='footballcoachcareerhistory',
            old_name='type',
            new_name='league_type',
        ),
        migrations.RemoveField(
            model_name='footballcoach',
            name='current_team_id',
        ),
        migrations.RemoveField(
            model_name='footballcoach',
            name='from_date',
        ),
        migrations.RemoveField(
            model_name='footballcoach',
            name='is_open_for_hiring',
        ),
        migrations.RemoveField(
            model_name='footballcoach',
            name='my_worth',
        ),
        migrations.RemoveField(
            model_name='footballcoach',
            name='playoffs_games_coached_in',
        ),
        migrations.RemoveField(
            model_name='footballcoach',
            name='playoffs_games_lost',
        ),
        migrations.RemoveField(
            model_name='footballcoach',
            name='playoffs_games_won',
        ),
        migrations.RemoveField(
            model_name='footballcoach',
            name='to_date',
        ),
        migrations.RemoveField(
            model_name='footballcoach',
            name='total_no_tournaments_won_as_coach',
        ),
        migrations.RemoveField(
            model_name='footballcoachcareerhistory',
            name='playoffs_games_coached_in',
        ),
        migrations.RemoveField(
            model_name='footballcoachcareerhistory',
            name='playoffs_games_lost',
        ),
        migrations.RemoveField(
            model_name='footballcoachcareerhistory',
            name='playoffs_games_won',
        ),
        migrations.RemoveField(
            model_name='footballcoachcareerhistory',
            name='total_no_tournaments_won_as_coach',
        ),
        migrations.AddField(
            model_name='footballcoach',
            name='certificate',
            field=models.ImageField(blank=True, null=True, upload_to='cerificate'),
        ),
        migrations.AddField(
            model_name='footballcoachcareerhistory',
            name='achievements',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='footballcoachcareerhistory',
            name='league_name',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]
