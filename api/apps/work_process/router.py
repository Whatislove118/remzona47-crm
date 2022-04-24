from rest_framework import routers

from .views import JobViewSet

router = routers.SimpleRouter()
router.register(r"jobs", JobViewSet)
