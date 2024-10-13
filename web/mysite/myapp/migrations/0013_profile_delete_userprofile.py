# Generated by Django 5.0.6 on 2024-10-13 14:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_remove_userprofile_user_id_userprofile_id'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='Anonymous', max_length=30)),
                ('surname', models.CharField(default='Anonymous', max_length=30)),
                ('phone_number', models.CharField(default='Anonymous', max_length=15)),
                ('student_ID', models.CharField(max_length=15, unique=True)),
                ('kku_mail', models.EmailField(max_length=100, unique=True)),
                ('dorm', models.CharField(default='Anonymous', max_length=30)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]