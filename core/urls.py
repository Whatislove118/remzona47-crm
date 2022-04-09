"""remzona URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'{settings.API_URL}schema/', SpectacularAPIView.as_view(), name='schema'),
    path(f'{settings.API_URL}swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path(f'{settings.API_URL}redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('auth/', include('dj_rest_auth.urls')),
    path('users/', include('rest_auth.urls')),
    path(f'{settings.API_URL}', include('api.urls')),
    path('', RedirectView.as_view(url=f'{settings.API_URL}swagger/')),
]
