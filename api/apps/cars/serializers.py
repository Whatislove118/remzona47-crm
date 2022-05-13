from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from rest_auth.serializers import ClientSerializer

from .models import Brand, Car, CarModel


class BrandSerializer(serializers.ModelSerializer):
    count_models = serializers.IntegerField()

    class Meta:
        model = Brand
        fields = "__all__"
        read_only_fields = [
            "id",
        ]


class CarModelSerializer(serializers.ModelSerializer):
    count_cars = serializers.IntegerField()
    brand = serializers.SlugRelatedField(
        many=False, slug_field="name", queryset=Brand.objects.all()
    )

    class Meta:
        model = CarModel
        fields = "__all__"
        read_only_fields = [
            "id",
        ]
        validators = [
            UniqueTogetherValidator(
                queryset=model.objects.all(), fields=["name", "brand"]
            )
        ]


class CarDetailsSerializer(serializers.ModelSerializer):
    model = CarModelSerializer(many=False, read_only=True)
    owner = ClientSerializer(many=False, read_only=True)

    class Meta:
        model = Car
        fields = "__all__"


class CarCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = "__all__"
        read_only_fields = [
            "id",
        ]
