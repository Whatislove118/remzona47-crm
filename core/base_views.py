from rest_framework.viewsets import ModelViewSet as DRFModelViewSet
from rest_framework.viewsets import \
    ReadOnlyModelViewSet as DRFReadOnlyModelViewSet
from rest_framework.decorators import action


class ModelViewSet(DRFModelViewSet):
    '''
        ModelViewSet from drf including drf-access-policy integration.
        Should set model attriibute
    '''
    @property
    def access_policy(self):
        return self.permission_classes[0]

    def get_queryset(self):
        return self.access_policy.scope_queryset(self.request, self.model.objects.all())


class ReadOnlyModelViewSet(DRFReadOnlyModelViewSet):
    '''
        ReadOnlyModelViewSet from drf including drf-access-policy integration.
        
    '''
    @property
    def access_policy(self):
        return self.permission_classes[0]

    def get_queryset(self):
        return self.access_policy.scope_queryset(self.request, self.model.objects.all())

class CountMixin:
    
    @action(methods=["GET"], detail=False)
    def count(self, request, *args, **kwargs):
        qs = self.get_queryset()
        return {"count": qs.count()}