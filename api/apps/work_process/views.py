from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (OpenApiParameter, extend_schema,
                                   extend_schema_view)
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet

from api.apps.work_process.models import Job

from .serializers import JobDetailsSerializer


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
    serializer_class = JobDetailsSerializer

    def filter_queryset(self, queryset):
        start = self.request.query_params.get("start", None)
        end = self.request.query_params.get("end", None)
        if start:
            start_date = serializers.DateTimeField().to_internal_value(start)
            self.queryset = self.queryset.filter(started_at__gt=start_date)
        if end:
            end_date = serializers.DateTimeField().to_internal_value(end)
            self.queryset = self.queryset.filter(started_at__lt=end_date)
        return queryset

    def perform_create(self, serializer):
        user = self.request.data.get("user")

        if user:
            serializer.save()
        return super().perform_create(serializer)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
