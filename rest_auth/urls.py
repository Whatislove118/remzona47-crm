
from django.urls import include, path
from .views import CreateStaffViewSet, GroupViewSet
from rest_framework.routers import SimpleRouter

'''
    urlpatterns with excluded routes
'''
router = SimpleRouter()
router.register('staff', CreateStaffViewSet)
router.register('groups', GroupViewSet)

urlpatterns = router.get_urls()
