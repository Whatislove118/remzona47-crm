# Generated by Django 4.0.3 on 2022-04-23 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_process', '0002_alter_job_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='status',
            field=models.CharField(choices=[('Открыта', 'Opened'), ('В работе', 'In Progress'), ('Выполнена', 'Resolved'), ('Отложена', 'Postpone')], default='Открыта', max_length=100),
        ),
    ]