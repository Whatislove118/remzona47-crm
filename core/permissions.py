from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAuthenticated

class IsAdminOrStaffUser(BasePermission):
    
    def has_permission(self, request, view):
        return bool(
            request.user and (request.user.is_superuser or request.user.is_staff)
        )
    
class IsAdminUser(BasePermission):
    
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_superuser
        )
        