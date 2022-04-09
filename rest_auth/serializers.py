from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()




class StaffCreateSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(
        many=True,
        slug_field="name",
        queryset=Group.objects.all()
    )
    
    class Meta:
        model = User
        exclude = ('is_superuser', 'last_login', 'date_joined', 'user_permissions', 'is_active')
        read_only_fields = ('id', )
    
    
