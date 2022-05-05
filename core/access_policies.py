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
            "principal": "staff",
            "effect": "allow",
        },
        {
            "action": ["create", "destroy"],
            "principal": [f"group:{settings.MODERATOR_GROUP_NAME}", "admin"],
            "effect": "allow",
        },
        {
            "action": ["update", "partial_update", "change_password"],
            "principal": "staff",
            "condition": "is_owner_or_superuser",
            "effect": "allow",
        },
    ]

    @classmethod
    def scope_queryset(cls, request, qs):
        return qs.filter(is_staff=True, is_superuser=False)


class JobAccessPolicy(BaseAccessPolicy):
    statements = [
        {
            "action": ["list", "retrieve", "statuses"],
            "principal": "staff",
            "effect": "allow",
        },
        {
            "action": ["create", "destroy", "partial_update", "update"],
            "principal": [f"group:{settings.MODERATOR_GROUP_NAME}", "admin"],
            "effect": "allow",
        },
    ]

    @classmethod
    def scope_queryset(cls, request, qs):
        if request.user.groups.filter(name=settings.REGULAR_USERS_GROUP_NAME).exists():
            qs = qs.filter(master=request.user)
        return qs


class FavourAccessPolicy(BaseAccessPolicy):
    statements = [
        {
            "action": ["list", "retrieve"],
            "principal": "staff",
            "effect": "allow",
        },
        {
            "action": ["create", "destroy", "partial_update", "update"],
            "principal": [f"group:{settings.MODERATOR_GROUP_NAME}", "admin"],
            "effect": "allow",
        },
    ]

    @classmethod
    def scope_queryset(cls, request, qs):
        return qs


class ClientAccessPolicy(BaseAccessPolicy):
    statements = [
        {
            "action": ["*"],
            "principal": [f"group:{settings.MODERATOR_GROUP_NAME}", "admin"],
            "effect": "allow",
        }
    ]

    @classmethod
    def scope_queryset(cls, request, qs):
        return qs


class AnalyticsAccessPolicy(BaseAccessPolicy):
    statements = [
        {
            "action": ["*"],
            "principal": [f"group:{settings.MODERATOR_GROUP_NAME}", "admin"],
            "effect": "allow",
        }
    ]

    @classmethod
    def scope_queryset(cls, request, qs):
        return qs


class BrandAccessPolicy(BaseAccessPolicy):
    statements = [
        {
            "action": ["list", "retrieve"],
            "principal": "staff",
            "effect": "allow",
        },
        {
            "action": ["create", "destroy", "partial_update", "update"],
            "principal": [f"group:{settings.MODERATOR_GROUP_NAME}", "admin"],
            "effect": "allow",
        },
    ]

    @classmethod
    def scope_queryset(cls, request, qs):
        return qs


class CarModelAccessPolicy(BrandAccessPolicy):
    pass


class CarAccessPolicy(BrandAccessPolicy):
    pass
