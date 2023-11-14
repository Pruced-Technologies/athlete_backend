# Generated by Django 4.2.4 on 2023-10-23 13:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0098_remove_reference_user_id_player_reference_inside_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='referenceoutside',
            old_name='user_id',
            new_name='player_id',
        ),
        migrations.RemoveField(
            model_name='player',
            name='agent_inside',
        ),
        migrations.RemoveField(
            model_name='player',
            name='reference_inside',
        ),
        migrations.AddField(
            model_name='agent',
            name='player_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agent_inside', to='football.player'),
        ),
        migrations.AddField(
            model_name='reference',
            name='player_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reference_users_inside', to='football.player'),
        ),
    ]
