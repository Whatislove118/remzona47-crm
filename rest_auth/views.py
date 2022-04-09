from django.contrib.auth import get_user_model, models
from yaml import serialize
from core import permissions
from rest_framework.viewsets import ModelViewSet
from .serializers import StaffSerializer, GroupSerializer
from rest_framework.decorators import action


User = get_user_model()

class CreateStaffViewSet(ModelViewSet):
    model = User
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser, ]
    serializer_class = StaffSerializer


class CreateClientViewSet(ModelViewSet):
    pass


class GroupViewSet(ModelViewSet):
    model = models.Group
    queryset = models.Group.objects.all()
    permission_classes = [permissions.IsAdminUser, ]
    serializer_class = GroupSerializer
