import uuid

from django.db import models

from core.mixins import OverloadedQuerysetManagerMixin


# Create your models here.
class Car(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        "rest_auth.Client",
        null=False,
        blank=False,
        related_name="cars",
        on_delete=models.CASCADE,
    )
    model = models.ForeignKey(
        "CarModel",
        null=False,
        blank=False,
        related_name="cars",
        on_delete=models.RESTRICT,
    )
    vin = models.CharField(max_length=25, null=False, blank=False)
    plate_number = models.CharField(max_length=20, null=False, blank=False)
    release_date = models.DateField()
    color_code = models.PositiveIntegerField(null=False)
    mileage = models.PositiveBigIntegerField(null=False)
    power = models.DecimalField(decimal_places=1, max_digits=4)
    engine_size = models.DecimalField(decimal_places=1, max_digits=2)

    class Meta:
        db_table = "cars"


class BrandManager(OverloadedQuerysetManagerMixin, models.Manager):
    def with_count_models(self):
        result = self.get_queryset().annotate(count_models=models.Count("models__id"))
        return result


class Brand(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)

    objects = BrandManager()

    class Meta:
        db_table = "car_brands"


class CarModelManager(OverloadedQuerysetManagerMixin, models.Manager):
    def with_count_cars(self):
        result = self.get_queryset().annotate(count_cars=models.Count("cars__id"))
        return result


class CarModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    brand = models.ForeignKey(
        "Brand",
        null=False,
        blank=False,
        related_name="models",
        on_delete=models.RESTRICT,
    )
    name = models.CharField(max_length=100, null=False, blank=False)

    objects = CarModelManager()

    class Meta:
        db_table = "car_models"
        constraints = [
            models.UniqueConstraint(fields=["brand", "name"], name="unique_brand_name")
        ]
