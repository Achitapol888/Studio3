# Generated by Django 5.0.6 on 2024-10-14 17:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_userprofile_preferences_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='preferences',
        ),
    ]
