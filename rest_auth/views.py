from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model, models
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    extend_schema,
    extend_schema_view,
)
from rest_framework import exceptions, serializers
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from core.access_policies import ClientAccessPolicy, StaffAccessPolicy
from core.base_views import ModelViewSet
from core.validation import ErrorMessages, Messages
from rest_auth.models import Client, Position, Worklogs

from .serializers import (
    ClientSerializer,
    GroupSerializer,
    PositionSerializer,
    StaffCreateSerializer,
    StaffDetailsSerializer,
    WorklogCreateSerializer,
    WorklogDetailsSerializer,
)

User = get_user_model()


@extend_schema(tags=["staff"])
class StaffViewSet(ModelViewSet):
    permission_classes = (StaffAccessPolicy,)
    model = User
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("first_name", "last_name", "email", "position__name")
    queryset = User.objects.all()
    serializer_class = StaffDetailsSerializer

    def get_serializer_class(self):
        if self.action == "create":
            self.serializer_class = StaffCreateSerializer
        return self.serializer_class

    def get_object(self):
        if self.action == "change_password":
            user_id = serializers.UUIDField().to_internal_value(data=self.kwargs["pk"])
            user = get_object_or_404(self.get_queryset(), id=user_id)
            return user
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
        user = self.get_object()
        if (
            user.id != request.user.id
            and not request.user.groups.filter(
                name=settings.MODERATOR_GROUP_NAME
            ).exists()
            and not request.user.is_superuser
        ):  # noqa
            raise exceptions.ValidationError(
                detail=ErrorMessages.PERMISSIONS_DENIED, code=403
            )
        password = request.data.get("password")
        if not password:
            raise exceptions.ValidationError(
                detail=ErrorMessages.EMPTY_FIELD.format("password")
            )
        user.set_password(password)
        user.save()
        return Response(Messages.PASSWORD_CHANGED)

    @action(methods=["GET"], detail=True)
    def salary(self, request, *args, **kwargs):
        user = self.get_object()
        


@extend_schema(tags=["clients"])
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                "newest", OpenApiTypes.BOOL, OpenApiParameter.QUERY, default=False
            ),
        ],
    ),
)
class ClientsViewSet(ModelViewSet):
    queryset = Client.objects.all()
    model = Client
    permission_classes = (ClientAccessPolicy,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("last_name", "phone_number")
    serializer_class = ClientSerializer

    def get_queryset(self):
        queryset = self.access_policy.scope_queryset(self.request, self.queryset)
        newest_param = self.request.query_params.get("newest")
        if newest_param:
            newest = serializers.BooleanField().to_internal_value(
                data=self.request.query_params.get("newest")
            )
            if newest:
                current_month = datetime.now().month
                queryset = queryset.filter(created_at__month=current_month)
        return queryset


@extend_schema(tags=["groups"])
class GroupViewSet(ModelViewSet):
    permission_classes = (StaffAccessPolicy,)
    model = models.Group
    queryset = models.Group.objects.all()
    serializer_class = GroupSerializer


@extend_schema(tags=["positions"])
class PositionViewSet(ModelViewSet):
    permission_classes = (StaffAccessPolicy,)
    model = Position
    queryset = Position.objects.all()
    serializer_class = PositionSerializer

    def perform_create(self, serializer):
        return super().perform_create(serializer)


@extend_schema(tags=["worklogs"])
class WorklogViewSet(ModelViewSet):
    permission_classes = (StaffAccessPolicy,)
    model = Worklogs
    queryset = Worklogs.objects.all()
    serializer_class = WorklogDetailsSerializer

    def get_serializer_class(self):
        if self.action == "create":
            self.serializer_class = WorklogCreateSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        user = self.request.user
        owner_id = self.request.data.get("user")
        if not owner_id:
            owner_id = self.request.user.id
        if user.has_group(name="master-regular") and owner_id != user.id:
            raise serializers.ValidationError(
                "Вы не можете логировать время за другого человека."
            )
        serializer.save(owner_id=owner_id)
