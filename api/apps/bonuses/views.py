from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from requests import Response
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from api.apps.bonuses.models import BalanceHistory, BonusBalance
from core.access_policies import BonusBalanceAccessPolicy
from core.base_views import ReadOnlyModelViewSet

from .serializers import BalanceHistorySerializer, BonusBalanceSerializer


class BonusBalanceViewSet(ReadOnlyModelViewSet):
    model = BonusBalance
    queryset = BonusBalance.objects.all()
    permission_classes = (BonusBalanceAccessPolicy,)
    filter_backends = (filters.DjangoFilterBackend,)
    serializer_class = BonusBalanceSerializer
    filterset_fields = ("client",)

    def get_serializer_class(self):
        if self.action in ("retrieve_history", "list_history"):
            self.serializer_class = BalanceHistorySerializer
        return super().get_serializer_class()

    def get_object(self):
        if self.action == "retrieve_history":
            obj = get_object_or_404(
                BalanceHistory.objects.all(), id=self.kwargs.get("pk")
            )
            return obj
        return super().get_object()

    def list(self, request, *args, **kwargs):
        raise MethodNotAllowed()

    @action(methods=["GET"], detail=True)
    def retrieve_history(self, request, *args, **kwargs):
        obj = self.get_object()
        result = self.get_serializer(obj)
        return Response(result.data)

    @action(methods=["GET"], detail=False)
    def list_history(self, request, *args, **kwargs):
        pass
