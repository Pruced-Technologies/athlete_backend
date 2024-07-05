# Generated by Django 4.2.4 on 2024-06-06 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0180_news_attending_persons'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='footballplayersandcoachesunderme',
            name='agent',
        ),
        migrations.AddField(
            model_name='footballplayersandcoachesunderme',
            name='agent_career_history',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='players_and_coaches_under_me', to='football.agentcareerhistory'),
        ),
    ]
