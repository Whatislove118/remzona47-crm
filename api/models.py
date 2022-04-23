import uuid
from django.db import models
from django.conf import settings



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

        