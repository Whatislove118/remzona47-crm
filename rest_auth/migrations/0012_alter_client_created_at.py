# Generated by Django 4.0.3 on 2022-05-10 12:29

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rest_auth", "0011_alter_client_created_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="created_at",
            field=models.DateTimeField(
                default=datetime.datetime(2022, 5, 10, 15, 29, 50, 937475)
            ),
        ),
    ]