from rest_framework import serializers
from api.serializers import PositionSerializer
from api.models import Position
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


User = get_user_model()


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        exclude = ['permissions', ]
        read_only_fields = ('id', )


class StaffSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=False, read_only=True)
    position = PositionSerializer(many=False, read_only=True)
    
    class Meta:
        model = User
        exclude = ('is_superuser', 'is_staff', 'last_login', 'date_joined', 'user_permissions', 'is_active')
        read_only_fields = ('id', 'salary')
        


class StaffCreateSerializer(StaffSerializer):
    groups = serializers.SlugRelatedField(
        many=True,
        slug_field="name",
        queryset=Group.objects.all(),
        required=False
    )
    position = serializers.SlugRelatedField(
        many=False,
        slug_field="name",
        queryset=Position.objects.all()
    )
    
    class Meta(StaffSerializer.Meta):
        pass
        
    
    def create(self, validated_data: dict) -> User:
        validated_data['is_staff'] = True
        if not validated_data.get('groups'):
            validated_data['groups'] = [Group.objects.get(name="master-regular")]
        return User.objects.create_user(**validated_data)

    





