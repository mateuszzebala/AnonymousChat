# Generated by Django 4.1.4 on 2022-12-29 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0009_remove_chat_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='disconnected',
            field=models.BooleanField(default=False),
        ),
    ]
