from django.contrib.auth import get_user_model, models
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import exceptions, serializers
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core import permissions
from core.access_policies import StaffAccessPolicy
from core.base_views import ModelViewSet
from core.validation import ErrorMessages, Messages
from rest_auth.models import Position, Worklogs

from .serializers import (GroupSerializer, PositionSerializer,
                          StaffCreateSerializer, StaffDetailsSerializer,
                          WorklogCreateSerializer, WorklogDetailsSerializer)

User = get_user_model()


@extend_schema(tags=["staff"])
class StaffViewSet(ModelViewSet):
    permission_classes = (StaffAccessPolicy,)
    model = User
    queryset = User.objects.staff()
    serializer_class = StaffDetailsSerializer

    def get_serializer_class(self):
        if self.action == "create":
            self.serializer_class = StaffCreateSerializer
        return self.serializer_class

    def get_object(self):
        if self.action == "change_password":
            user_id = serializers.UUIDField().to_internal_value(data=self.kwargs["pk"])
            try:
                user = self.model.objects.get(id=user_id)
                return user
            except self.model.DoesNotExist:
                raise NotFound()
        return super().get_object()

    @extend_schema(
        methods=["POST"],
        responses={200: OpenApiTypes.STR, 400: OpenApiTypes.OBJECT},
        examples=[
            OpenApiExample(
                name="Change staff password",
                value={"password": "password"},
                request_only=True,
            )
        ],
    )
    @action(methods=["POST"], detail=True)
    def change_password(self, request, *args, **kwargs):
        user = request.user
        password = request.data.get("password")
        if not password:
            raise exceptions.ValidationError(
                detail=ErrorMessages.EMPTY_FIELD.format("password")
            )
        user.set_password(password)
        user.save()
        return Response(Messages.PASSWORD_CHANGED)


class CreateClientViewSet(ModelViewSet):
    pass


@extend_schema(tags=["groups"])
class GroupViewSet(ModelViewSet):
    model = models.Group
    queryset = models.Group.objects.all()
    permission_classes = [
        permissions.IsAdminUser,
    ]
    serializer_class = GroupSerializer


@extend_schema(tags=["positions"])
class PositionViewSet(ModelViewSet):
    model = Position
    queryset = Position.objects.all()
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = PositionSerializer

    def perform_create(self, serializer):
        return super().perform_create(serializer)


@extend_schema(tags=["worklogs"])
class WorklogViewSet(ModelViewSet):
    model = Worklogs
    queryset = Worklogs.objects.all()
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = WorklogDetailsSerializer

    def get_serializer_class(self):
        if self.action == "create":
            self.serializer_class = WorklogCreateSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        user = self.request.user
        user_id = self.request.data.get("user")
        if not user_id:
            user_id = self.request.user.id
        if user.has_group(name="master-regular") and user_id != user.id:
            raise serializers.ValidationError(
                "Вы не можете логировать время за другого человека."
            )
        serializer.save(user_id=user_id)
