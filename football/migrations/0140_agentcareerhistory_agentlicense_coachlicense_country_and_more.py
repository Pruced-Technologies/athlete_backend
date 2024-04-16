# Generated by Django 4.2.4 on 2024-04-10 04:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0139_alter_player_primary_position_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgentCareerHistory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('from_year', models.IntegerField(blank=True, null=True)),
                ('to_year', models.IntegerField(blank=True, null=True)),
                ('company', models.CharField(blank=True, max_length=255, null=True)),
                ('contact_no', models.CharField(blank=True, max_length=12, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('address_lane', models.CharField(blank=True, max_length=255, null=True)),
                ('zip', models.CharField(blank=True, max_length=25, null=True)),
                ('state', models.CharField(blank=True, max_length=255, null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('achievements', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AgentLicense',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('license_id', models.IntegerField(blank=True, null=True)),
                ('license_name', models.CharField(blank=True, max_length=255, null=True)),
                ('certificate', models.ImageField(blank=True, null=True, upload_to='cerificate')),
            ],
        ),
        migrations.CreateModel(
            name='CoachLicense',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('license_id', models.IntegerField(blank=True, null=True)),
                ('license_name', models.CharField(blank=True, max_length=255, null=True)),
                ('certificate', models.ImageField(blank=True, null=True, upload_to='cerificate')),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('country_name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='FootballPlayersAndCoachesUnderMe',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sport_profile', models.CharField(blank=True, max_length=25, null=True)),
                ('user_id', models.IntegerField(blank=True, null=True)),
                ('user_name', models.CharField(blank=True, max_length=100, null=True)),
                ('is_notable', models.BooleanField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sport_type', models.TextField()),
                ('league_name', models.CharField(max_length=255)),
                ('league_type', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SportLicense',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('license_name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('club_name', models.CharField(max_length=255)),
                ('reg_id', models.CharField(max_length=50)),
                ('country_name', models.CharField(blank=True, max_length=255, null=True)),
                ('sport_type', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='agentoutside',
            name='player_id',
        ),
        migrations.RemoveField(
            model_name='playercareerhistory',
            name='player_id',
        ),
        migrations.RemoveField(
            model_name='reference',
            name='player_id',
        ),
        migrations.RemoveField(
            model_name='reference',
            name='reffered_user',
        ),
        migrations.RemoveField(
            model_name='referenceoutside',
            name='player_id',
        ),
        migrations.RenameField(
            model_name='club',
            old_name='league',
            new_name='league_name',
        ),
        migrations.RenameField(
            model_name='club',
            old_name='type',
            new_name='league_type',
        ),
        migrations.RenameField(
            model_name='footballcoachcareerhistory',
            old_name='league',
            new_name='country_name',
        ),
        migrations.RenameField(
            model_name='footballcoachcareerhistory',
            old_name='playoffs_games_coached_in',
            new_name='from_year',
        ),
        migrations.RenameField(
            model_name='footballcoachcareerhistory',
            old_name='playoffs_games_lost',
            new_name='league_id',
        ),
        migrations.RenameField(
            model_name='footballcoachcareerhistory',
            old_name='type',
            new_name='league_type',
        ),
        migrations.RenameField(
            model_name='footballcoachcareerhistory',
            old_name='playoffs_games_won',
            new_name='to_year',
        ),
        migrations.RemoveField(
            model_name='agent',
            name='player_id',
        ),
        migrations.RemoveField(
            model_name='club',
            name='period',
        ),
        migrations.RemoveField(
            model_name='footballcoach',
            name='current_team',
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
            name='period',
        ),
        migrations.RemoveField(
            model_name='footballcoachcareerhistory',
            name='total_no_tournaments_won_as_coach',
        ),
        migrations.RemoveField(
            model_name='type',
            name='player_type',
        ),
        migrations.AddField(
            model_name='agent',
            name='country_name',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='club',
            name='achievements',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='club',
            name='country_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='club',
            name='from_year',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='club',
            name='league_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='club',
            name='to_year',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='footballcoachcareerhistory',
            name='achievements',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='footballcoachcareerhistory',
            name='league_name',
            field=models.CharField(blank=True, max_length=225, null=True),
        ),
        migrations.AddField(
            model_name='sportprofiletype',
            name='priority',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='pin',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='agent',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agent', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='footballcoachcareerhistory',
            name='club_name',
            field=models.CharField(blank=True, max_length=225, null=True),
        ),
        migrations.AlterField(
            model_name='type',
            name='sport_type',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.DeleteModel(
            name='Acheivements',
        ),
        migrations.DeleteModel(
            name='AgentOutside',
        ),
        migrations.DeleteModel(
            name='PlayerCareerHistory',
        ),
        migrations.DeleteModel(
            name='Reference',
        ),
        migrations.DeleteModel(
            name='ReferenceOutside',
        ),
        migrations.AddField(
            model_name='footballplayersandcoachesunderme',
            name='agent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='players_and_coaches_under_me', to='football.agent'),
        ),
        migrations.AddField(
            model_name='coachlicense',
            name='coach',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='my_license', to='football.footballcoach'),
        ),
        migrations.AddField(
            model_name='agentlicense',
            name='agent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='my_license', to='football.agent'),
        ),
        migrations.AddField(
            model_name='agentcareerhistory',
            name='agent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='career_history', to='football.agent'),
        ),
    ]
