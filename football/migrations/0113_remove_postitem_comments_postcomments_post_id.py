# Generated by Django 4.2.4 on 2023-12-05 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0112_postcomments_postitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postitem',
            name='comments',
        ),
        migrations.AddField(
            model_name='postcomments',
            name='post_id',
            field=models.ManyToManyField(blank=True, related_name='comments', to='football.postitem'),
        ),
    ]
