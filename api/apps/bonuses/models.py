from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from model_utils.fields import UUIDField

from core.mixins import ValidationMixin


class BonusBalance(ValidationMixin, models.Model):
    id = UUIDField()
    updated_at = models.DateTimeField(auto_now=True)
    client = models.OneToOneField(
        "rest_auth.Client",
        null=False,
        blank=False,
        related_name="bonuses",
        on_delete=models.CASCADE,
    )
    balance = models.PositiveBigIntegerField(default=0)

    class Meta:
        db_table = "bonus_balance"


class BalanceHistory(models.Model):
    id = UUIDField()
    created_at = models.DateTimeField(auto_now_add=True)
    bonus_balance = models.ForeignKey(
        BonusBalance,
        null=False,
        blank=False,
        related_name="history",
        on_delete=models.CASCADE,
    )
    value = models.IntegerField(null=False, blank=False)

    class Meta:
        db_table = "balance_history"


@receiver(signal=pre_save, sender=BonusBalance)
def create_balance_history(sender, instance, created=False, **kwargs):
    """
    Signal for autocreating history on changed balance
    """
    if not created:
        db_instance = sender.objects.get(id=instance.id)
        value = instance.balance - db_instance.balance
        BalanceHistory.objects.create(bonus_balance_id=instance.id, value=value)
