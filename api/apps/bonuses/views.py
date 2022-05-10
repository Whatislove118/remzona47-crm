from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    extend_schema,
    extend_schema_view,
)
from rest_framework import exceptions, serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from api.apps.bonuses.models import BalanceHistory, BonusBalance
from core.access_policies import BalanceHistoryAccessPolicy, BonusBalanceAccessPolicy
from core.base_views import ReadOnlyModelViewSet

from .serializers import BalanceHistorySerializer, BonusBalanceSerializer


@extend_schema(
    tags=["balance"],
)
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter("client_id", OpenApiTypes.UUID, OpenApiParameter.QUERY),
        ],
    ),
)
class BonusBalanceViewSet(ReadOnlyModelViewSet):
    model = BonusBalance
    queryset = BonusBalance.objects.all()
    permission_classes = (BonusBalanceAccessPolicy,)
    serializer_class = BonusBalanceSerializer

    def get_queryset(self):
        queryset = self.access_policy.scope_queryset(self.request, self.queryset)
        client = self.request.query_params.get("client_id", None)
        if client:
            client_id = serializers.UUIDField().to_internal_value(data=client)
            queryset = queryset.filter(client_id=client_id)
        return queryset

    @extend_schema(
        methods=["POST"],
        responses={201: serializer_class, 400: OpenApiTypes.OBJECT},
        examples=[
            OpenApiExample(
                name="success",
                request_only=True,
                value={"bonuses": 0},
            )
        ],
    )
    @action(methods=["POST"], detail=True)
    def change(self, request, *args, **kwargs):
        bonuses = self.request.data.get("bonuses", None)
        serializers.IntegerField().to_internal_value(data=bonuses)
        if bonuses == 0:
            raise exceptions.ValidationError(
                detail="Количество бонусов должно быть больше 0"
            )
        obj = self.get_object()
        obj.balance += bonuses
        obj.save()
        obj.run_validators()
        serializer = self.get_serializer(obj)
        return Response(data=serializer.data)


@extend_schema(
    tags=["bonuses-history"],
)
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter("balance_pk", OpenApiTypes.UUID, OpenApiParameter.QUERY),
            OpenApiParameter("client_id", OpenApiTypes.UUID, OpenApiParameter.QUERY),
            OpenApiParameter("first_name", OpenApiTypes.STR, OpenApiParameter.QUERY),
            OpenApiParameter("last_name", OpenApiTypes.STR, OpenApiParameter.QUERY),
            OpenApiParameter("phone_number", OpenApiTypes.STR, OpenApiParameter.QUERY),
        ],
    ),
)
class BalanceHistoryViewSet(ReadOnlyModelViewSet):
    model = BalanceHistory
    queryset = BalanceHistory.objects.all()
    permission_classes = (BalanceHistoryAccessPolicy,)
    serializer_class = BalanceHistorySerializer

    def get_queryset(self):
        queryset = self.access_policy.scope_queryset(self.request, self.queryset)
        balance = self.request.query_params.get("balance_pk", None)
        first_name = self.request.query_params.get("first_name", None)
        last_name = self.request.query_params.get("last_name", None)
        phone_number = self.request.query_params.get("phone_number", None)
        client = self.request.query_params.get("client_id", None)

        if first_name:
            queryset = queryset.filter(bonus_balance__client__first_name=first_name)

        if last_name:
            queryset = queryset.filter(bonus_balance__client__last_name=last_name)

        if phone_number:
            queryset = queryset.filter(bonus_balance__client__phone_number=phone_number)

        if balance:
            balance_id = serializers.UUIDField().to_internal_value(data=balance)
            queryset = queryset.filter(bonus_balance_id=balance_id)

        if client:
            client_id = serializers.UUIDField().to_internal_value(data=client)
            queryset = queryset.filter(bonus_balance__client_id=client_id)

        return queryset
