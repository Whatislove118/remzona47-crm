from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model

User = get_user_model()




class StaffCreateSerializer(ModelSerializer):
    
    class Meta:
        model = User
        exclude = ('is_superuser', 'last_login', 'date_joined', 'groups', 'user_permissions', 'is_active')
        read_only_fields = ('id', )
    
    
