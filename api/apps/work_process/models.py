from datetime import datetime
import uuid
from django.db import models
from core import utils
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class JobStatus(models.Choices):
    opened = "Открыта"
    in_progress = "В работе"
    resolved = "Выполнена"
    postpone = "Отложена"
    

class JobManager(models.Manager):
    
    def jobs_by_month(self, start_date, end_date):
        # current_month = utils.month_by_number(month)
        # next_month = utils.month_by_number(month + 1)
        return self.get_queryset().filter()
        

class Favour(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=100, decimal_places=2)
    
    class Meta:
        db_table = "favours"

class Job(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    favour = models.ForeignKey(
        Favour,
        related_name="jobs", 
        blank=False,
        null=False,
        on_delete=models.RestrictedError
    ) 
    master = models.ForeignKey(
        User,
        related_name="jobs",
        blank=False,
        null=False,
        on_delete=models.RestrictedError
    )
    description = models.TextField()
    started_at = models.DateTimeField(null=False, blank=False)
    ended_at = models.DateTimeField(null=False, blank=False)
    
    client = None
    status = models.CharField(
        max_length=100,
        choices=JobStatus.choices,
        default=JobStatus.opened
    )
    
    objects = JobManager()
    
    class Meta:
        db_table = "jobs"
        

