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

class IsResourceOwner(BasePermission):
    
    def has_permission(self, request, view):
        return bool(
            request.user or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            
        )
        return super().has_object_permission(request, view, obj)
    
# '''
#     Permissions description of base user groups
# '''


# MODERATOR_PERMISSIONS = (
#     "__all__",
# )

# REGULAR_PERMISSIONS = (
#     "view_jobs",
#     "create_worklogs",
#     "view_worklogs",
#     "delete_worklogs",
#     "change_worklogs",
#     "view_staff",
# )
