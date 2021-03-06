# Generated by Django 4.0.3 on 2022-05-05 17:18

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("rest_auth", "0006_alter_client_created_at"),
    ]

    operations = [
        migrations.CreateModel(
            name="Brand",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
            ],
            options={
                "db_table": "car_brands",
            },
        ),
        migrations.CreateModel(
            name="CarModel",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "brand",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="models",
                        to="cars.brand",
                    ),
                ),
            ],
            options={
                "db_table": "car_models",
            },
        ),
        migrations.CreateModel(
            name="Car",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("vin", models.CharField(max_length=25)),
                ("plate_number", models.CharField(max_length=20)),
                ("release_date", models.DateField()),
                ("color_code", models.PositiveIntegerField()),
                ("mileage", models.PositiveBigIntegerField()),
                ("power", models.DecimalField(decimal_places=1, max_digits=4)),
                ("engine_size", models.DecimalField(decimal_places=1, max_digits=2)),
                (
                    "model",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="cars",
                        to="cars.carmodel",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cars",
                        to="rest_auth.client",
                    ),
                ),
            ],
            options={
                "db_table": "cars",
            },
        ),
        migrations.AddConstraint(
            model_name="carmodel",
            constraint=models.UniqueConstraint(
                fields=("brand", "name"), name="unique_brand_name"
            ),
        ),
    ]
