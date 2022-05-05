from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (OpenApiParameter, extend_schema,
                                   extend_schema_view)
from rest_framework import serializers

from api.apps.work_process.models import Favour, Job
from core.access_policies import FavourAccessPolicy, JobAccessPolicy
from core.base_views import CountMixin, ModelViewSet
from rest_framework.decorators import action
from .serializers import (FavourSerializer, JobCreateSerializer,
                          JobDetailsSerializer)
from rest_framework.response import Response


@extend_schema(
    tags=["jobs"],
)
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter("start", OpenApiTypes.DATETIME, OpenApiParameter.QUERY),
            OpenApiParameter("end", OpenApiTypes.DATETIME, OpenApiParameter.QUERY),
            OpenApiParameter("status", OpenApiTypes.STR, OpenApiParameter.QUERY),
            OpenApiParameter("master", OpenApiTypes.ANY, OpenApiParameter.QUERY)
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
            queryset = queryset.filter(started_at__lte=end_date, ended_at__gte=start_date)

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
        master_id = self.request.data.get("master")
        if not master_id:
            master_id = user.id
        if user.has_group(name="master-regular") and master_id != user.id:
            raise serializers.ValidationError(
                "Вы не можете назначать задачу другому человеку."
            )
        serializer.save(master_id=master_id)


@extend_schema(
    tags=["favours"],
)
class FavourViewSet(ModelViewSet):
    queryset = Favour.objects.all()
    model = Favour
    permission_classes = (FavourAccessPolicy,)
    serializer_class = FavourSerializer

    # def perform_create(self, serializer):
    #     user = self.request.user
    #     master_id = self.request.data.get("master")
    #     if not master_id:
    #         master_id = user.id
    #     if user.has_group(name="master-regular") and master_id != user.id:
    #         raise serializers.ValidationError(
    #             "Вы не можете назначать задачу другому человеку."
    #         )
    #     serializer.save(master_id=master_id)
