from .views import CreateStaffViewSet, GroupViewSet, PositionViewSet, WorklogViewSet
from rest_framework.routers import SimpleRouter

'''
    urlpatterns with excluded routes
'''
router = SimpleRouter()
router.register(r'staff/worklogs', WorklogViewSet)
router.register(r'staff/positions', PositionViewSet)
router.register(r'staff', CreateStaffViewSet)
router.register(r'groups', GroupViewSet)



urlpatterns = router.get_urls()
