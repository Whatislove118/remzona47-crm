from django.urls import include, path
from rest_framework import routers
from .views import PositionViewSet, WorklogViewSet, health

router = routers.SimpleRouter()
router.register(r'positions', PositionViewSet)
router.register(r'worklogs', WorklogViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('health/', health)
]
