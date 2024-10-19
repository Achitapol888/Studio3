# Generated by Django 5.1.2 on 2024-10-18 07:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0009_postgiver_is_matched_postreceiver_is_matched"),
    ]

    operations = [
        migrations.AlterField(
            model_name="matchhistory",
            name="giver_post",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="match_histories_giver_post",
                to="myapp.postgiver",
            ),
        ),
        migrations.AlterField(
            model_name="matchhistory",
            name="receiver_post",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="match_histories_receiver_post",
                to="myapp.postreceiver",
            ),
        ),
    ]