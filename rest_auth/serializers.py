from rest_framework import serializers
from api.serializers import PositionSerializer
from api.models import Position
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from dj_rest_auth.serializers import UserDetailsSerializer as DjUserDetailSerializer


UserModel = get_user_model()


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        exclude = ['permissions', ]
        read_only_fields = ('id', )


class UserDetailsSerializer(DjUserDetailSerializer):
    groups = GroupSerializer(many=True, read_only=True)

    class Meta(DjUserDetailSerializer.Meta):
        extra_fields = []
        # see https://github.com/iMerica/dj-rest-auth/issues/181
        # UserModel.XYZ causing attribute error while importing other
        # classes from `serializers.py`. So, we need to check whether the auth model has
        # the attribute or not
        if hasattr(UserModel, 'USERNAME_FIELD'):
            extra_fields.append(UserModel.USERNAME_FIELD)
        if hasattr(UserModel, 'EMAIL_FIELD'):
            extra_fields.append(UserModel.EMAIL_FIELD)
        if hasattr(UserModel, 'first_name'):
            extra_fields.append('first_name')
        if hasattr(UserModel, 'last_name'):
            extra_fields.append('last_name')
        if hasattr(UserModel, "groups"):
            extra_fields.append("groups")
        model = UserModel
        fields = ('pk', *extra_fields)
        read_only_fields = ('email',)

class StaffSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)
    position = PositionSerializer(many=False, read_only=True)
    
    class Meta:
        model = UserModel
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
        
    
    def create(self, validated_data: dict) -> UserModel:
        validated_data['is_staff'] = True
        if not validated_data.get('groups'):
            validated_data['groups'] = [Group.objects.get(name="master-regular")]
        return UserModel.objects.create_user(**validated_data)

    





