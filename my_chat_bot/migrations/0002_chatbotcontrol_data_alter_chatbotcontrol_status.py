# Generated by Django 4.2.13 on 2024-07-07 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_chat_bot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatbotcontrol',
            name='data',
            field=models.JSONField(default='{}'),
        ),
        migrations.AlterField(
            model_name='chatbotcontrol',
            name='status',
            field=models.CharField(default=''),
        ),
    ]
