from django.urls import include, path
from rest_framework import routers
from .views import health
from .apps.work_process.router import router as jobs_router
api_router = routers.SimpleRouter()


urlpatterns = [
    path('', include(api_router.urls)),
    path('health/', health)
]
urlpatterns += jobs_router.get_urls()
