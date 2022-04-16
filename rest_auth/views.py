from django.contrib.auth import get_user_model, models
from core import permissions
from rest_framework.viewsets import ModelViewSet
from .serializers import StaffCreateSerializer, StaffSerializer, GroupSerializer
from rest_framework.decorators import action


User = get_user_model()

class CreateStaffViewSet(ModelViewSet):
    model = User
    queryset = User.objects.staff()
    permission_classes = [permissions.IsAdminUser, ]
    serializer_class = StaffSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            self.serializer_class = StaffCreateSerializer
        return self.serializer_class


class CreateClientViewSet(ModelViewSet):
    pass


class GroupViewSet(ModelViewSet):
    model = models.Group
    queryset = models.Group.objects.all()
    permission_classes = [permissions.IsAdminUser, ]
    serializer_class = GroupSerializer

    