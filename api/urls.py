from django.urls import include, path
from rest_framework import routers

from .apps.analytics.router import router as analytics_router
from .apps.cars.router import router as cars_router
from .apps.work_process.router import router as jobs_router
from .views import health

api_router = routers.SimpleRouter()


urlpatterns = [path("", include(api_router.urls)), path("health/", health)]
urlpatterns += jobs_router.get_urls()
urlpatterns += analytics_router.get_urls()
urlpatterns += cars_router.get_urls()
