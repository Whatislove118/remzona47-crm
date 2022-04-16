import uuid
from django.db import models
from django.conf import settings


# class Master(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
#     salary = models.DecimalField(default=0, decimal_places=2, max_digits=10)
#     position = models.ForeignKey('Position', related_name="masters", null=True, blank=True, on_delete=models.RESTRICT)
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="master", null=False, blank=False, on_delete=models.CASCADE)
    
#     class Meta:
#         db_table = 'masters'
        
    
class PositionManager(models.Manager):
    pass

class Position(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    rate = models.PositiveIntegerField(default=0) # rate per hour 
    description = models.TextField()
    
    objects = PositionManager()
    
    class Meta:
        db_table = "positions"
        

class Worklogs(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, blank=False, on_delete=models.CASCADE)
    timeworked = models.DecimalField(max_digits=100, decimal_places=2)
    
    class Meta:
        db_table = "worklogs"

class Car(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    model = models.ForeignKey("CarModel", null=False, blank=False, related_name="cars", on_delete=models.RESTRICT)
    vin = models.CharField(max_length=15, null=False, blank=False)
    plate_number = models.CharField(max_length=20, null=False, blank=False)
    release_date = models.DateField()
    power = models.DecimalField(decimal_places=1, max_digits=4)
    engine_size = models.DecimalField(decimal_places=1, max_digits=2)
    


class Brand(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)


class CarModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    brand = models.ForeignKey("Brand", null=False, blank=False, related_name="models", on_delete=models.RESTRICT)
    name = name = models.CharField(max_length=100, null=False, blank=False)

        