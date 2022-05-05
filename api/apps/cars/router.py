from rest_framework import routers

from .views import BrandViewSet, CarModelViewSet, CarViewSet

router = routers.SimpleRouter()
router.register(r"cars/brands", BrandViewSet)
router.register(r"cars/models", CarModelViewSet)
router.register(r"cars", CarViewSet)
