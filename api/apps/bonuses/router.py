from rest_framework import routers

from api.apps.bonuses.views import BalanceHistoryViewSet, BonusBalanceViewSet

app_name = "bonuses"

router = routers.SimpleRouter()
router.register(r"bonuses/balances", BonusBalanceViewSet)
router.register(r"bonus/balances/history", BalanceHistoryViewSet)
