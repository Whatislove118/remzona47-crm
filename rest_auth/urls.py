from rest_framework.routers import SimpleRouter

from .views import GroupViewSet, PositionViewSet, StaffViewSet, WorklogViewSet, ClientsViewSet

"""
    urlpatterns with excluded routes
"""
router = SimpleRouter()
router.register(r"staff/worklogs", WorklogViewSet)
router.register(r"staff/positions", PositionViewSet)
router.register(r"staff", StaffViewSet)
router.register(r"groups", GroupViewSet)
router.register(r"clients", ClientsViewSet)


urlpatterns = router.get_urls()
