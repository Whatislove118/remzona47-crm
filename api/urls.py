from django.urls import include, path
from rest_framework import routers
from .views import PositionViewSet, health

router = routers.SimpleRouter()
router.register(r'positions', PositionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('health/', health)
]
