# Generated by Django 4.0.3 on 2022-05-08 17:08

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rest_auth", "0009_alter_client_created_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="created_at",
            field=models.DateTimeField(
                default=datetime.datetime(2022, 5, 8, 20, 8, 17, 804153)
            ),
        ),
    ]