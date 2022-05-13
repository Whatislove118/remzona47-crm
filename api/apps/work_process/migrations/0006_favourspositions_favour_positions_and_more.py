# Generated by Django 4.0.3 on 2022-05-10 16:13

import uuid

import django.db.models.deletion
import model_utils.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rest_auth", "0013_alter_client_created_at"),
        ("work_process", "0005_job_client"),
    ]

    operations = [
        migrations.CreateModel(
            name="FavoursPositions",
            fields=[
                (
                    "id",
                    model_utils.fields.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
            ],
            options={
                "db_table": "favours_positions",
            },
        ),
        migrations.AddField(
            model_name="favour",
            name="positions",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="favours",
                through="work_process.FavoursPositions",
                to="rest_auth.position",
            ),
        ),
        migrations.AddField(
            model_name="favourspositions",
            name="favour_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RestrictedError,
                to="work_process.favour",
            ),
        ),
        migrations.AddField(
            model_name="favourspositions",
            name="position_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RestrictedError,
                to="rest_auth.position",
            ),
        ),
        migrations.AddConstraint(
            model_name="favourspositions",
            constraint=models.UniqueConstraint(
                fields=("favour_id", "position_id"), name="unique_favour_id_position_id"
            ),
        ),
    ]