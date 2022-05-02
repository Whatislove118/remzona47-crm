# Generated by Django 4.0.3 on 2022-05-02 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_process', '0002_remove_job_ended_at_remove_job_started_at_job_end_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='end',
        ),
        migrations.RemoveField(
            model_name='job',
            name='start',
        ),
        migrations.AddField(
            model_name='job',
            name='ended_at',
            field=models.DateTimeField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='job',
            name='started_at',
            field=models.DateTimeField(default=None),
            preserve_default=False,
        ),
    ]
