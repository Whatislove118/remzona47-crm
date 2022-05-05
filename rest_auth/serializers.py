from dj_rest_auth.serializers import \
    UserDetailsSerializer as DjUserDetailSerializer
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers

from rest_auth.models import Client, Position, Worklogs

UserModel = get_user_model()


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"
        read_only_fields = ("id", "created_at")


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        exclude = [
            "permissions",
        ]
        read_only_fields = ("id",)


class UserDetailsSerializer(DjUserDetailSerializer):
    groups = GroupSerializer(many=True, read_only=True)

    class Meta(DjUserDetailSerializer.Meta):
        extra_fields = []
        # see https://github.com/iMerica/dj-rest-auth/issues/181
        # UserModel.XYZ causing attribute error while importing other
        # classes from `serializers.py`. So, we need to check whether the auth model has
        # the attribute or not
        if hasattr(UserModel, "USERNAME_FIELD"):
            extra_fields.append(UserModel.USERNAME_FIELD)
        if hasattr(UserModel, "EMAIL_FIELD"):
            extra_fields.append(UserModel.EMAIL_FIELD)
        if hasattr(UserModel, "first_name"):
            extra_fields.append("first_name")
        if hasattr(UserModel, "last_name"):
            extra_fields.append("last_name")
        if hasattr(UserModel, "groups"):
            extra_fields.append("groups")
        model = UserModel
        fields = ("pk", "is_superuser", *extra_fields)
        read_only_fields = ("email",)


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = "__all__"
        read_only_fields = ("id",)


class WorklogCreateSerializer(serializers.ModelSerializer):
    timeworked = serializers.CharField()

    # def validate_timeworked(self, value):
    #     pattern = r"([1-9]+[h|m])+"

    class Meta:
        model = Worklogs
        fields = "__all__"
        read_only_fields = ("id",)
        extra_kwargs = {"owner": {"required": False}}


class WorklogDetailsSerializer(WorklogCreateSerializer):
    owner = UserDetailsSerializer(many=False)

    class Meta(WorklogCreateSerializer.Meta):
        model = Worklogs
        fields = "__all__"
        read_only_fields = ("id",)
        extra_kwargs = {"owner": {"required": False}}


class StaffDetailsSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)
    position = PositionSerializer(many=False, read_only=True)

    class Meta:
        model = UserModel
        exclude = (
            "is_superuser",
            "is_staff",
            "last_login",
            "date_joined",
            "user_permissions",
            "is_active",
            "password",
        )
        read_only_fields = ("id", "salary")


class StaffCreateSerializer(StaffDetailsSerializer):
    groups = serializers.SlugRelatedField(
        many=True, slug_field="name", queryset=Group.objects.all(), required=False
    )
    position = serializers.SlugRelatedField(
        many=False, slug_field="name", queryset=Position.objects.all()
    )

    class Meta(StaffDetailsSerializer.Meta):
        exclude = (
            "is_superuser",
            "is_staff",
            "last_login",
            "date_joined",
            "user_permissions",
            "is_active",
        )

    def create(self, validated_data: dict) -> UserModel:
        validated_data["is_staff"] = True
        if not validated_data.get("groups"):
            validated_data["groups"] = [Group.objects.get(name=settings.REGULAR_USERS_GROUP_NAME)]
        return UserModel.objects.create_user(**validated_data)
