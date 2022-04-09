from rest_framework.viewsets import ModelViewSet
from .models import Position
from core import permissions
from .serializers import PositionSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import Group
from rest_framework.exceptions import ValidationError

class PositionViewSet(ModelViewSet):
    model = Position
    queryset = Position.objects.all()
    permission_classes = (permissions.IsAdminUser, )
    serializer_class = PositionSerializer
    
    def perform_create(self, serializer):
        return super().perform_create(serializer)
    
    



@api_view(['GET'])
def health(request):
    if request.method == 'GET':
        return Response({'detail': 'ok'})