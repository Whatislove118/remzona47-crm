# Generated by Django 4.0.3 on 2022-05-10 12:29

import uuid

import django.db.models.deletion
import model_utils.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("rest_auth", "0012_alter_client_created_at"),
    ]

    operations = [
        migrations.CreateModel(
            name="BonusBalance",
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
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("balance", models.PositiveBigIntegerField(default=0)),
                (
                    "client",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bonuses",
                        to="rest_auth.client",
                    ),
                ),
            ],
            options={
                "db_table": "bonus_balance",
            },
        ),
        migrations.CreateModel(
            name="BalanceHistory",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "status",
                    model_utils.fields.StatusField(
                        choices=[
                            ("Пополнение", "Пополнение"),
                            ("Списание", "Списание"),
                        ],
                        db_index=True,
                        default="Пополнение",
                        max_length=100,
                        no_check_for_status=True,
                    ),
                ),
                ("value", models.PositiveBigIntegerField()),
                (
                    "bonus_balance",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="history",
                        to="bonuses.bonusbalance",
                    ),
                ),
            ],
            options={
                "db_table": "balance_history",
            },
        ),
    ]
