# Generated by Django 5.1.2 on 2024-10-19 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0019_postreceiver_is_confirm"),
    ]

    operations = [
        migrations.AddField(
            model_name="postgiver",
            name="is_confirm",
            field=models.BooleanField(default=False),
        ),
    ]