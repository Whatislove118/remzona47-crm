from .views import StaffViewSet, GroupViewSet, PositionViewSet, WorklogViewSet
from rest_framework.routers import SimpleRouter

'''
    urlpatterns with excluded routes
'''
router = SimpleRouter()
router.register(r'staff/worklogs', WorklogViewSet)
router.register(r'staff/positions', PositionViewSet)
router.register(r'staff', StaffViewSet)
router.register(r'groups', GroupViewSet)



urlpatterns = router.get_urls()
