from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet as DRFModelViewSet
from rest_framework.viewsets import \
    ReadOnlyModelViewSet as DRFReadOnlyModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin


class PolicyMixin:
    
    @property
    def access_policy(self):
        return self.permission_classes[0]

    def get_queryset(self):
        return self.access_policy.scope_queryset(self.request, self.model.objects.all())


class ModelViewSet(PolicyMixin, DRFModelViewSet):
    """
    ModelViewSet from drf including drf-access-policy integration.
    Should set model attriibute
    """
    pass


class ReadOnlyModelViewSet(PolicyMixin, DRFReadOnlyModelViewSet):
    """
    ReadOnlyModelViewSet from drf including drf-access-policy integration.

    """
    pass


class ListModelViewSet(PolicyMixin, ListModelMixin, GenericViewSet):
    pass


class CountMixin:
    @action(methods=["GET"], detail=False)
    def count(self, request, *args, **kwargs):
        qs = self.get_queryset()
        return {"count": qs.count()}
