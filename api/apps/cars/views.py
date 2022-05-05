from django_filters import rest_framework as filters
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view

from core.access_policies import (
    BrandAccessPolicy,
    CarAccessPolicy,
    CarModelAccessPolicy,
)
from core.base_views import ModelViewSet

from .models import Brand, Car, CarModel
from .serializers import (
    BrandSerializer,
    CarCreateSerializer,
    CarDetailsSerializer,
    CarModelSerializer,
)


@extend_schema(
    tags=["brands"],
)
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter("name", OpenApiTypes.STR, OpenApiParameter.QUERY),
        ],
    ),
)
class BrandViewSet(ModelViewSet):
    model = Brand
    permission_classes = (BrandAccessPolicy,)
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("name",)


@extend_schema(
    tags=["car_models"],
)
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter("name", OpenApiTypes.STR, OpenApiParameter.QUERY),
            OpenApiParameter("brand__name", OpenApiTypes.STR, OpenApiParameter.QUERY),
        ],
    ),
)
class CarModelViewSet(ModelViewSet):
    model = CarModel
    permission_classes = (CarModelAccessPolicy,)
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("name", "brand__name")


@extend_schema(
    tags=["cars"],
)
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter("vin", OpenApiTypes.STR, OpenApiParameter.QUERY),
            OpenApiParameter(
                "owner__first_name", OpenApiTypes.STR, OpenApiParameter.QUERY
            ),
            OpenApiParameter(
                "owner__last_name", OpenApiTypes.STR, OpenApiParameter.QUERY
            ),
            OpenApiParameter(
                "owner__phone_number", OpenApiTypes.STR, OpenApiParameter.QUERY
            ),
            OpenApiParameter("model__name", OpenApiTypes.STR, OpenApiParameter.QUERY),
            OpenApiParameter(
                "model__brand__name", OpenApiTypes.STR, OpenApiParameter.QUERY
            ),
        ],
    ),
)
class CarViewSet(ModelViewSet):
    model = Car
    permission_classes = (CarAccessPolicy,)
    queryset = Car.objects.all()
    serializer_class = CarDetailsSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = (
        "vin",
        "owner__first_name",
        "owner__last_name",
        "owner__phone_number",
        "model__name",
        "model__brand__name",
    )

    def get_serializer_class(self):
        if self.action == "create":
            self.serializer_class = CarCreateSerializer
        return super().get_serializer_class()
