from django.contrib.auth import get_user_model
from django.db import models
from model_utils import Choices
from model_utils.fields import StatusField, UUIDField

User = get_user_model()


class Favour(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=100, decimal_places=2)

    class Meta:
        db_table = "favours"


class JobManager(models.Manager):
    def count_by_status(self, status):
        res = (
            self.get_queryset()
            .values("status")
            .filter(status=status)
            .annotate(count=models.Count("id"))
            .first()
        )
        if res is None:
            res = {"status": status, "count": 0}
        return res


class Job(models.Model):
    id = UUIDField(primary_key=True, version=4, editable=False)
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

    client = models.ForeignKey(
        "rest_auth.Client",
        related_name="jobs",
        null=True,
        blank=True,
        on_delete=models.RestrictedError,
    )

    STATUS = Choices(
        "Открыта",
        "В работе",
        "Выполнена",
        "Отложена",
    )
    status = StatusField(default="opened", db_index=True)

    objects = JobManager()

    @property
    def owner(self):
        """
        To match in access_policy
        """
        return self.master

    class Meta:
        db_table = "jobs"
