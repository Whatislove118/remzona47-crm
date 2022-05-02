# Create your views here.
from api.apps.analytics.serializers import AnalyticsUserWorklogsSerializer
from core.base_views import ModelViewSet
from core.access_policies import AnalyticsAccessPolicy
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response

UserModel = get_user_model()


@extend_schema(tags=["analytics"])
class AnalyticsUserWorklogsViewSet(ModelViewSet):
    model = UserModel
    queryset = UserModel.objects.all()
    permission_classes = (AnalyticsAccessPolicy, )
    serializer_class = AnalyticsUserWorklogsSerializer
    
    def list(self, request, *args, **kwargs):
        users = self.model.objects.users_worklogs_exp()
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data)
    