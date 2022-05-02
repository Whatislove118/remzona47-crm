from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
    extend_schema_view
)
from rest_framework import serializers
from core.access_policies import FavourAccessPolicy, JobAccessPolicy
from core.base_views import ModelViewSet

from api.apps.work_process.models import Favour, Job
from rest_auth.models import Client

from .serializers import FavourSerializer, JobCreateSerilizer, JobDetailsSerializer


@extend_schema(
    tags=["jobs"],
)
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter("start", OpenApiTypes.DATETIME, OpenApiParameter.QUERY),
            OpenApiParameter("end", OpenApiTypes.DATETIME, OpenApiParameter.QUERY),
        ],
    ),
)
class JobViewSet(ModelViewSet):
    queryset = Job.objects.all()
    permission_classes = (JobAccessPolicy,)
    serializer_class = JobDetailsSerializer
    model = Job
    
    def get_serializer_class(self):
        if self.action == "create":
            self.serializer_class = JobCreateSerilizer
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = self.access_policy.scope_queryset(self.request, self.queryset)
        start = self.request.query_params.get("start", None)
        end = self.request.query_params.get("end", None)
        if start:
            start_date = serializers.DateTimeField().to_internal_value(start)
            queryset = queryset.filter(started_at__gte=start_date)
        if end:
            end_date = serializers.DateTimeField().to_internal_value(end)
            queryset = queryset.filter(ended_at__lte=end_date)
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

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

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