from django.contrib.auth import get_user_model
from core import permissions
from rest_framework.viewsets import ModelViewSet
from .serializers import StaffCreateSerializer

User = get_user_model()

class CreateStaffViewSet(ModelViewSet):
    model = User
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser, ]
    serializer_class = StaffCreateSerializer
    
    def create(self, request, *args, **kwargs):
        
        return super().create(request, *args, **kwargs)
    

class CreateClientViewSet(ModelViewSet):
    pass