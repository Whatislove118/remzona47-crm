from rest_framework import routers

from api.apps.bonuses.views import BonusBalanceViewSet

router = routers.SimpleRouter()
router.register(r"bonuses")
