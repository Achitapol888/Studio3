# Generated by Django 5.0.6 on 2024-10-18 06:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_rename_dorm_postreceiver_user_profile_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_matched', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('giver_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match_histories', to='myapp.postgiver')),
                ('receiver_post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='match_histories', to='myapp.postreceiver')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.userprofile')),
            ],
        ),
    ]