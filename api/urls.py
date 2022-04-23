from django.urls import include, path
from rest_framework import routers
from .views import health

router = routers.SimpleRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('health/', health)
]
