# Generated by Django 4.0.3 on 2022-05-02 13:52

import datetime
import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rest_auth", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="client",
            name="created_at",
            field=models.DateTimeField(
                default=datetime.datetime(2022, 5, 2, 16, 52, 47, 411609)
            ),
        ),
        migrations.AlterField(
            model_name="client",
            name="id",
            field=models.UUIDField(
                default=uuid.UUID("d67f3470-3d5e-47f2-84ac-7be4bebb0feb"),
                editable=False,
                primary_key=True,
                serialize=False,
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="id",
            field=models.UUIDField(
                default=uuid.UUID("ba962421-eb83-4749-8016-3c4c1d4f1ffc"),
                editable=False,
                primary_key=True,
                serialize=False,
            ),
        ),
    ]
