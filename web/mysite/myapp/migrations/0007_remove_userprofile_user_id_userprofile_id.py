# Generated by Django 5.0.6 on 2024-10-13 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_remove_userprofile_id_userprofile_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user_ID',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='id',
            field=models.BigAutoField(auto_created=True, default='not defined', primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
