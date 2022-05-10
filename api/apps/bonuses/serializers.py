from rest_framework import serializers

from rest_auth.serializers import ClientSerializer

from .models import BalanceHistory, BonusBalance


class BonusBalanceSerializer(serializers.ModelSerializer):
    client = ClientSerializer(many=False, read_only=True)

    class Meta:
        model = BonusBalance
        fields = "__all__"
        read_only_fields = [
            "id",
            "updated_at",
            "balance",
        ]


class BalanceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BalanceHistory
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_at",
            "value",
        ]
