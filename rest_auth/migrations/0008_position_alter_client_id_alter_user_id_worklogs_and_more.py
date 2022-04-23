# Generated by Django 4.0.3 on 2022-04-23 14:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('rest_auth', '0007_alter_client_id_alter_user_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Worklogs',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('timeworked', models.DecimalField(decimal_places=2, max_digits=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'worklogs',
            },
        ),
    ]
