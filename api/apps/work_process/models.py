import uuid

from django.contrib.auth import get_user_model
from django.db import models



User = get_user_model()


class JobStatus(models.Choices):
    opened = "Открыта"
    in_progress = "В работе"
    resolved = "Выполнена"
    postpone = "Отложена"


class JobManager(models.Manager):

    pass


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
        on_delete=models.RestrictedError,
    )
    master = models.ForeignKey(
        User,
        related_name="jobs",
        blank=False,
        null=False,
        on_delete=models.RestrictedError,
    )
    description = models.TextField()
    started_at = models.DateTimeField(null=False, blank=False)
    ended_at = models.DateTimeField(null=False, blank=False)

    client = None
    status = models.CharField(
        max_length=100, choices=JobStatus.choices, default=JobStatus.opened
    )

    objects = JobManager()

    @property
    def owner(self):
        """
        To match in access_policy
        """
        return self.master

    class Meta:
        db_table = "jobs"


