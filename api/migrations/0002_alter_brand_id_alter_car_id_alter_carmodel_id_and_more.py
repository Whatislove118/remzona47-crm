# Generated by Django 4.0.3 on 2022-04-09 13:58

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='id',
            field=models.UUIDField(default=uuid.UUID('01733d54-e34b-4838-97c3-92944c3c9354'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='car',
            name='id',
            field=models.UUIDField(default=uuid.UUID('23997ece-c6cb-44e2-8ce1-4f338cc91c64'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='carmodel',
            name='id',
            field=models.UUIDField(default=uuid.UUID('9b92c43a-081d-4b6c-9584-f68704bbd7d4'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='master',
            name='id',
            field=models.UUIDField(default=uuid.UUID('58cf6a6b-2def-465f-b27a-c1c24c10d3c5'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='position',
            name='id',
            field=models.UUIDField(default=uuid.UUID('3ea6368a-e351-4b6b-bb15-f0ce80198b4a'), editable=False, primary_key=True, serialize=False),
        ),
    ]