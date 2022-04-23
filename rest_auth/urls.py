
from django.urls import include, path
from .views import CreateStaffViewSet, GroupViewSet, PositionViewSet, WorklogViewSet
from rest_framework.routers import SimpleRouter

'''
    urlpatterns with excluded routes
'''
router = SimpleRouter()
router.register(r'staff', CreateStaffViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'positions', PositionViewSet)
router.register(r'worklogs', WorklogViewSet)

urlpatterns = router.get_urls()
