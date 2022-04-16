from rest_framework.viewsets import ModelViewSet
from rest_framework import serializers
from .models import Position, Worklogs
from core import permissions
from .serializers import PositionSerializer, WorklogSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import Group
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model


User = get_user_model

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


@api_view(['GET'])
def health(request):
    if request.method == 'GET':
        return Response({'detail': 'ok'})