# Generated by Django 4.0.3 on 2022-05-10 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rest_auth", "0013_alter_client_created_at"),
        ("work_process", "0006_favourspositions_favour_positions_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="favour",
            name="positions",
            field=models.ManyToManyField(
                blank=True,
                related_name="favours",
                through="work_process.FavoursPositions",
                to="rest_auth.position",
            ),
        ),
    ]
