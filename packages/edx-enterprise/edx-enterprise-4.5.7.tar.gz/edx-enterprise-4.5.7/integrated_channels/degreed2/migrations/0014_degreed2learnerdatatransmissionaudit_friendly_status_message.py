# Generated by Django 3.2.15 on 2022-09-13 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('degreed2', '0013_auto_20220523_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='degreed2learnerdatatransmissionaudit',
            name='friendly_status_message',
            field=models.CharField(blank=True, default=None, help_text='A user-friendly API response status message.', max_length=255, null=True),
        ),
    ]
