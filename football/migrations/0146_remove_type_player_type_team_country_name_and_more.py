# Generated by Django 4.2.4 on 2024-03-15 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0145_alter_league_country_id_alter_team_league_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='type',
            name='player_type',
        ),
        migrations.AddField(
            model_name='team',
            name='country_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='sport_type',
            field=models.ManyToManyField(blank=True, to='football.type'),
        ),
        migrations.AlterField(
            model_name='country',
            name='country_name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='reg_id',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='type',
            name='sport_type',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
