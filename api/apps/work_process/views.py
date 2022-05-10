from django.conf import settings
from django_filters import rest_framework as filters
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import serializers

from api.apps.work_process.models import Favour, Job, Workplaces
from core.access_policies import (
    AdminAccessPolicies,
    FavourAccessPolicy,
    JobAccessPolicy,
)
from core.base_views import CountMixin, ModelViewSet, ReadOnlyModelViewSet

from .serializers import (
    FavourCreateSerializer,
    FavourDetailsSerializer,
    JobCreateSerializer,
    JobDetailsSerializer,
    WorkplacesSerializer,
)


@extend_schema(
    tags=["jobs"],
)
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter("start", OpenApiTypes.DATETIME, OpenApiParameter.QUERY),
            OpenApiParameter("end", OpenApiTypes.DATETIME, OpenApiParameter.QUERY),
            OpenApiParameter("status", OpenApiTypes.STR, OpenApiParameter.QUERY),
            OpenApiParameter("master", OpenApiTypes.ANY, OpenApiParameter.QUERY),
        ],
    ),
)
class JobViewSet(CountMixin, ModelViewSet):
    queryset = Job.objects.all()
    permission_classes = (JobAccessPolicy,)
    serializer_class = JobDetailsSerializer
    model = Job

    def get_serializer_class(self):
        if self.action == "create":
            self.serializer_class = JobCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = super().get_queryset()

        start = self.request.query_params.get("start", None)
        end = self.request.query_params.get("end", None)
        status = self.request.query_params.get("status", None)
        master = self.request.query_params.get("master", None)

        if start and end:
            start_date = serializers.DateTimeField().to_internal_value(start)
            end_date = serializers.DateTimeField().to_internal_value(end)
            queryset = queryset.filter(
                started_at__lte=end_date, ended_at__gte=start_date
            )

        if status:
            queryset = queryset.filter(status=status)
        if master:
            try:
                master_id = serializers.UUIDField().to_internal_value(data=master)
                queryset = queryset.filter(master_id=master_id)
            except serializers.ValidationError:
                # username field
                queryset.filter(master__username=master)
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        if user.has_group(name=settings.REGULAR_USERS_GROUP_NAME):
            raise serializers.ValidationError(
                "Вы не можете назначать задачу другому человеку."
            )
        serializer.save()


@extend_schema(
    tags=["favours"],
)
class FavourViewSet(ModelViewSet):
    queryset = Favour.objects.all()
    model = Favour
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("name", "positions__name")
    permission_classes = (FavourAccessPolicy,)
    serializer_class = FavourDetailsSerializer

    def get_serializer_class(self):
        if self.action == "create":
            self.serializer_class = FavourCreateSerializer
        return super().get_serializer_class()


@extend_schema(tags=["workplaces"])
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter("start", OpenApiTypes.DATETIME, OpenApiParameter.QUERY),
            OpenApiParameter("end", OpenApiTypes.DATETIME, OpenApiParameter.QUERY),
        ],
    ),
)
class WorkplacesViewSet(ModelViewSet):
    queryset = Workplaces.objects.all()
    model = Workplaces
    permission_classes = (AdminAccessPolicies,)
    serializer_class = WorkplacesSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        start = self.request.query_params.get("start", None)
        end = self.request.query_params.get("end", None)
        if start and end:
            start_date = serializers.DateTimeField().to_internal_value(start)
            end_date = serializers.DateTimeField().to_internal_value(end)
            queryset = Workplaces.objects.available_by_jobs(start_date, end_date)
        return queryset
