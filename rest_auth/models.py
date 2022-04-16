import uuid
from django.db import models
from django.contrib.auth.models import UserManager as UManager, AbstractUser

from rest_auth.helpers import validate_credentials

class UserManager(UManager):

    def _create_user(self, username, email, password, **extra_fields):
        validate_credentials(username, email, password)
        groups = extra_fields.pop('groups')
        user = self.model(username=username, email=self.normalize_email(email), **extra_fields)
        if groups:
            user.groups.set(groups)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(username, email, password, **extra_fields)
    
    def staff(self):
        return self.get_queryset().filter(is_staff=True, is_superuser=False).all()


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    patronomic = models.CharField(max_length=15, null=True, blank=True)
    salary = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    position = models.ForeignKey('api.Position', related_name="users", null=True, blank=True, on_delete=models.RESTRICT)
        
    objects = UserManager()
    class Meta:
        db_table = 'users'
        
    
    def has_group(self, name):
        return self.groups.filter(name=name).count() != 0 

class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    first_name = models.CharField(max_length=20, null=False, blank=False)
    last_name = models.CharField(max_length=20, null=False, blank=False)
    patronomic = models.CharField(max_length=20, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=False, blank=False, unique=True)
    
    class Meta:
        db_table = 'clients'
