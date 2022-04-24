from django.urls import include, path
from rest_framework import routers

from .apps.work_process.router import router as jobs_router
from .views import health

api_router = routers.SimpleRouter()


urlpatterns = [path("", include(api_router.urls)), path("health/", health)]
urlpatterns += jobs_router.get_urls()
