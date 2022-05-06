from django.db import models
from model_utils.fields import StatusField, UUIDField


class BonusBalance(models.Model):
    id = UUIDField()
    updated_at = models.DateTimeField(auto_now=True)
    client = models.ForeignKey(
        "rest_auth.Client",
        null=False,
        blank=False,
        related_name="bonuses",
        on_delete=models.CASCADE,
    )
    balance = models.PositiveBigIntegerField(default=0)

    class Meta:
        db_table = "bonus_balance"


class BalanceHistorySerializer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    bonus_balance = models.ForeignKey(
        BonusBalance,
        null=False,
        blank=False,
        related_name="history",
        on_delete=models.CASCADE,
    )
    OPERATION = ("Пополнение", "Списание")
    operation = StatusField(db_index=True)
    value = models.PositiveBigIntegerField(null=False, blank=False)

    class Meta:
        db_table = "balance_history"
