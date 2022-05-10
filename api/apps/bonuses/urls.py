from rest_framework import routers

from api.apps.bonuses.views import BalanceHistoryViewSet, BonusBalanceViewSet

app_name = "bonuses"

router = routers.SimpleRouter()
router.register(r"bonuses/balances", BonusBalanceViewSet)
router.register(r"bonus/balances/history", BalanceHistoryViewSet)
# balance_router = NestedSimpleRouter(
#     router,
#     r"bonuses/balances",
#     lookup="balance",
# )
# balance_router.register(
#     r"histories",
#     BalanceHistoryViewSet,
#     basename="balance_history",
# )
# urlpatterns = [
#     path("bonuses/balances/histories/", BalanceHistoryViewSet.as_view({"get": "list"})),
#     path("", include(router.urls)),
#     path("", include(balance_router.urls)),
# ]
