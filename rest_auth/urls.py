
from django.urls import include, path
from .views import CreateStaffViewSet

'''
    urlpatterns with excluded routes
'''
urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('users/create/', CreateStaffViewSet.as_view({"post": "create"}))
]