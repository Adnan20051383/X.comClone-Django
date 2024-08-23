# Generated by Django 5.0.7 on 2024-08-22 13:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notif', '0002_notification_tweet'),
        ('tweet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='tweet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tweet.tweet'),
        ),
    ]