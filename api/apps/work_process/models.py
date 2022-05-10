from django.contrib.auth import get_user_model
from django.db import models
from model_utils import Choices
from model_utils.fields import StatusField, UUIDField

User = get_user_model()


class FavoursPositions(models.Model):
    id = UUIDField()
    favour = models.ForeignKey(
        "work_process.Favour",
        blank=False,
        null=False,
        on_delete=models.RestrictedError,
    )
    position = models.ForeignKey(
        "rest_auth.Position",
        blank=False,
        null=False,
        on_delete=models.RestrictedError,
    )

    class Meta:
        db_table = "favours_positions"
        constraints = [
            models.UniqueConstraint(
                fields=["favour_id", "position_id"], name="unique_favour_id_position_id"
            )
        ]


class Favour(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=100, decimal_places=2)
    positions = models.ManyToManyField(
        "rest_auth.Position",
        through="work_process.FavoursPositions",
        related_name="favours",
        blank=True,
    )

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
    workplace = models.ForeignKey(
        "work_process.Workplaces",
        related_name="jobs",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

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


class WorkplacesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related("jobs")

    def available_by_jobs(self, start, end):
        res = (
            self.get_queryset()
            .exclude(
                id__in=self.get_queryset().filter(
                    jobs__workplace_id=models.F("id"),
                    jobs__started_at__lte=start,
                    jobs__ended_at__gte=end,
                )
            )
            .annotate(available_date_start=models.F("jobs__ended_at"))
        )
        return res


class Workplaces(models.Model):
    is_available = models.BooleanField(default=True)

    objects = WorkplacesManager()

    class Meta:
        db_table = "workplaces"
