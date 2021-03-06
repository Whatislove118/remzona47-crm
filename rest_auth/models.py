from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as UManager
from django.db import models
from model_utils.fields import UUIDField

from rest_auth.helpers import validate_credentials


class UserManager(UManager):
    def _create_user(self, username, email, password, **extra_fields):
        validate_credentials(username, email, password)
        groups = extra_fields.pop("groups", None)
        user = self.model(
            username=username, email=self.normalize_email(email), **extra_fields
        )
        if groups:
            user.groups.set(groups)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(username, email, password, **extra_fields)

    def staff(self):
        return self.get_queryset().filter(is_staff=True, is_superuser=False).all()

    def users_worklogs_exp(self):
        users = self.get_queryset().filter(is_superuser=False)
        for user in users:
            user.total_worklogs, *_ = user.worklogs.total_exp(user).values()
        return users


class User(AbstractUser):
    id = UUIDField(primary_key=True, version=4, editable=False)
    patronomic = models.CharField(max_length=15, null=True, blank=True)
    salary = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    position = models.ForeignKey(
        "rest_auth.Position",
        related_name="users",
        null=True,
        blank=True,
        on_delete=models.RESTRICT,
    )

    objects = UserManager()

    class Meta:
        db_table = "users"

    def has_group(self, name):
        return self.groups.filter(name=name).count() != 0

    def salary(self):
        for worklog in self.worklogs.all():
            pass


class Client(models.Model):
    id = UUIDField(primary_key=True, version=4, editable=False)
    first_name = models.CharField(max_length=20, null=False, blank=False)
    last_name = models.CharField(max_length=20, null=False, blank=False)
    patronomic = models.CharField(max_length=20, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=False, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "clients"


class PositionManager(models.Manager):
    pass


class Position(models.Model):
    id = UUIDField(primary_key=True, version=4, editable=False)
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    rate = models.PositiveIntegerField(default=0)  # rate per hour
    description = models.TextField()

    objects = PositionManager()

    class Meta:
        db_table = "positions"


class WorklogsManager(models.Manager):
    use_for_related_fields = True

    def total_exp(self, user):
        return (
            self.get_queryset()
            .filter(owner_id=user.id)
            .aggregate(models.Sum("timeworked"))
        )


class Worklogs(models.Model):
    id = UUIDField(primary_key=True, version=4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="worklogs",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )
    timeworked = models.DecimalField(max_digits=100, decimal_places=2)
    objects = WorklogsManager()

    class Meta:
        db_table = "worklogs"


# @receiver(pre_save, sender=User)
# def user_change_password_signal(sender, **kwargs):
#     if not kwargs.get("created"):
#         user = kwargs.get('instance', None)
#         if user:
#             new_password = user.password
#             try:
#                 old_password = User.objects.get(pk=user.pk).password
#             except User.DoesNotExist:
#                 old_password = None
#             if new_password != old_password:
#                 user.set_password(new_password)
