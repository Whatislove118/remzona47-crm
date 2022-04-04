from rest_framework.viewsets import ModelViewSet
from .models import Position
from core import permissions
from .serializers import PositionSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

class PositionViewSet(ModelViewSet):
    model = Position
    queryset = Position.objects.all()
    permission_classes = (permissions.IsAdminUser, )
    serializer_class = PositionSerializer
    
    



@api_view(['GET'])
def health(request):
    if request.method == 'GET':
        return Response({'detail': 'ok'})