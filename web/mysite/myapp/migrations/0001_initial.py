# Generated by Django 5.0.6 on 2024-09-30 09:21

import django.contrib.postgres.fields
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
            name='Dorm',
            fields=[
                ('dorm_ID', models.AutoField(primary_key=True, serialize=False)),
                ('dorm_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('prefer_items', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), default=list, size=5)),
                ('history', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), default=list, size=5)),
                ('student_ID', models.CharField(max_length=15, unique=True)),
                ('kku_mail', models.EmailField(max_length=100, unique=True)),
                ('dorm', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.dorm')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('post_ID', models.AutoField(primary_key=True, serialize=False)),
                ('post_type', models.CharField(choices=[('giver', 'Giver'), ('receiver', 'Receiver')], max_length=10)),
                ('item_type', models.CharField(max_length=100)),
                ('item_name', models.CharField(max_length=100)),
                ('photo_image', models.ImageField(upload_to='images/')),
                ('detail', models.CharField(max_length=300)),
                ('quantity', models.IntegerField()),
                ('flaw', models.CharField(max_length=300)),
                ('date_limit', models.DateTimeField()),
                ('post_time', models.TimeField()),
                ('dorm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.dorm')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('chat_ID', models.AutoField(primary_key=True, serialize=False)),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to='myapp.userprofile')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to='myapp.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Verify',
            fields=[
                ('verify_ID', models.AutoField(primary_key=True, serialize=False)),
                ('verify_status', models.BooleanField(default=False)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.post')),
                ('verifier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('review_ID', models.AutoField(primary_key=True, serialize=False)),
                ('score', models.FloatField()),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.userprofile')),
                ('verify', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.verify')),
            ],
        ),
    ]
