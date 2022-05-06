from rest_framework import serializers

from .models import BalanceHistory, BonusBalance


class BonusBalanceSerializer(serializers.ModelSerializer):
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
