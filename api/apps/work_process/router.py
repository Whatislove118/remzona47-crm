from rest_framework import routers

from .views import FavourViewSet, JobViewSet

router = routers.SimpleRouter()
router.register(r"jobs", JobViewSet)
router.register(r"favours", FavourViewSet)