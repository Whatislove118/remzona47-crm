# Create your views here.
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response

from api.apps.analytics.serializers import (
    AnalyticsJobsSerializer,
    AnalyticsUserWorklogsSerializer,
)
from api.apps.work_process.models import Job
from core.access_policies import AnalyticsAccessPolicy
from core.base_views import ListModelViewSet

UserModel = get_user_model()


@extend_schema(tags=["analytics"])
class AnalyticsUserWorklogsViewSet(ListModelViewSet):
    model = UserModel
    queryset = UserModel.objects.all()
    permission_classes = (AnalyticsAccessPolicy,)
    serializer_class = AnalyticsUserWorklogsSerializer

    def list(self, request, *args, **kwargs):
        users = self.model.objects.users_worklogs_exp()
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data)


@extend_schema(tags=["analytics"])
class AnalyticsJobsViewSet(ListModelViewSet):
    model = Job
    queryset = model.objects.all()
    permission_classes = (AnalyticsAccessPolicy,)
    serializer_class = AnalyticsJobsSerializer

    def list(self, request, *args, **kwargs):
        aggregated_jobs = []
        for _, status in self.model.STATUS:
            aggregated_jobs.append(self.model.objects.count_by_status(status=status))
        serializer = self.serializer_class(aggregated_jobs, many=True)
        return Response(serializer.data)
