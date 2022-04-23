from django.contrib.auth import get_user_model, models
from core import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework import serializers
from rest_auth.models import Position, Worklogs
from .serializers import (
    StaffCreateSerializer,
    StaffDetailsSerializer,
    GroupSerializer,
    PositionSerializer,
    WorklogSerializer
)
from rest_framework.decorators import action


User = get_user_model()

class CreateStaffViewSet(ModelViewSet):
    model = User
    queryset = User.objects.staff()
    permission_classes = [permissions.IsAdminUser, ]
    serializer_class = StaffDetailsSerializer
    
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


class PositionViewSet(ModelViewSet):
    model = Position
    queryset = Position.objects.all()
    permission_classes = (permissions.IsAdminUser, )
    serializer_class = PositionSerializer
    
    def perform_create(self, serializer):
        return super().perform_create(serializer)
    
    
class WorklogViewSet(ModelViewSet):
    model = Worklogs
    queryset = Worklogs.objects.all()
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = WorklogSerializer
    
    
    def perform_create(self, serializer):
        user = self.request.user
        user_id = self.request.data.get('user')
        if not user_id:
            user_id = self.request.user.id
        if user.has_group(name="master-regular") and user_id != user.id:
            raise serializers.ValidationError("Вы не можете логировать время за другого человека.")
        serializer.save(user_id=user_id)