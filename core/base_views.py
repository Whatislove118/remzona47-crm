from rest_framework.viewsets import (
    ReadOnlyModelViewSet as DRFReadOnlyModelViewSet,
    ModelViewSet as DRFModelViewSet,
)

class ModelViewSet(DRFModelViewSet):
    
    @property
    def access_policy(self):
        return self.permission_classes[0]

    def get_queryset(self):
        return self.access_policy.scope_queryset(
            self.request, self.model.objects.all()
    )


class ReadOnlyModelViewSet(DRFReadOnlyModelViewSet):
    
    @property
    def access_policy(self):
        return self.permission_classes[0]

    def get_queryset(self):
        return self.access_policy.scope_queryset(
            self.request, self.model.objects.all()
    )