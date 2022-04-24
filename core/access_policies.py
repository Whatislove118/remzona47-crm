from django.conf import settings
from rest_access_policy import AccessPolicy


class BaseAccessPolicy(AccessPolicy):
    def is_owner_or_superuser(self, request, view, action) -> bool:
        obj = view.get_object()
        return request.user.is_superuser or (obj.owner == request.user)

    @classmethod
    def scope_queryset(cls, request, qs):
        if request.user.groups.filter(name=settings.MODERATOR_GROUP_NAME).exists():
            return qs

        return qs.filter(owner=request.user)


class StaffAccessPolicy(BaseAccessPolicy):
    statements = [
        {
            "action": ["list", "retrieve"],
            "principal": "authenticated",
            "effect": "allow",
        },
        {
            "action": ["create", "destroy"],
            "principal": [f"group:{settings.MODERATOR_GROUP_NAME}", "admin"],
            "effect": "allow",
        },
        {
            "action": ["update", "partial_update", "change_password"],
            "principal": "authenticated",
            "condition": "is_owner_or_superuser",
            "effect": "allow",
        },
    ]

    @classmethod
    def scope_queryset(cls, request, qs):
        return qs
