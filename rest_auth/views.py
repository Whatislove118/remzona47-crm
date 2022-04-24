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
    WorklogDetailsSerializer,
    WorklogCreateSerializer,
)
from drf_spectacular.utils import extend_schema


User = get_user_model()

@extend_schema(tags=['staff']) 
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

@extend_schema(tags=['tags']) 
class GroupViewSet(ModelViewSet):
    model = models.Group
    queryset = models.Group.objects.all()
    permission_classes = [permissions.IsAdminUser, ]
    serializer_class = GroupSerializer


@extend_schema(tags=['positions']) 
class PositionViewSet(ModelViewSet):
    model = Position
    queryset = Position.objects.all()
    permission_classes = (permissions.IsAdminUser, )
    serializer_class = PositionSerializer
    
    def perform_create(self, serializer):
        return super().perform_create(serializer)
    
    
@extend_schema(tags=['worklogs']) 
class WorklogViewSet(ModelViewSet):
    model = Worklogs
    queryset = Worklogs.objects.all()
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = WorklogDetailsSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            self.serializer_class = WorklogCreateSerializer
        return super().get_serializer_class()
    
    def perform_create(self, serializer):
        user = self.request.user
        user_id = self.request.data.get('user')
        if not user_id:
            user_id = self.request.user.id
        if user.has_group(name="master-regular") and user_id != user.id:
            raise serializers.ValidationError("Вы не можете логировать время за другого человека.")
        serializer.save(user_id=user_id)