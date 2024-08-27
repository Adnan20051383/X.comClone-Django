# Generated by Django 5.0.7 on 2024-08-27 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('msg', '0002_msg_is_seen'),
    ]

    operations = [
        migrations.AddField(
            model_name='msgsession',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='msg',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='msg_images/'),
        ),
    ]
