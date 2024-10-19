# Generated by Django 5.1.2 on 2024-10-19 13:14

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0015_matchedpost"),
    ]

    operations = [
        migrations.CreateModel(
            name="MatchPost",
            fields=[
                ("match_ID", models.AutoField(primary_key=True, serialize=False)),
                ("match_date", models.DateTimeField(default=django.utils.timezone.now)),
                ("is_confirmed", models.BooleanField(default=False)),
                ("confirmation_date", models.DateTimeField(blank=True, null=True)),
                (
                    "giver_post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="myapp.postgiver",
                    ),
                ),
                (
                    "receiver_post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="myapp.postreceiver",
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="MatchedPost",
        ),
    ]
