# Generated by Django 5.0.6 on 2024-10-13 15:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('first_name', models.CharField(default='Anonymous', max_length=30)),
                ('surname', models.CharField(default='Anonymous', max_length=30)),
                ('phone_number', models.CharField(default='Anonymous', max_length=15)),
                ('student_ID', models.CharField(max_length=15, primary_key=True, serialize=False, unique=True)),
                ('kku_mail', models.EmailField(max_length=100, unique=True)),
                ('dorm', models.CharField(default='Anonymous', max_length=30)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
