from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import MonthSerializer
from api.work_process.models import Job
from core import permissions, utils
# Create your views here.


class CalendarViewSet(ReadOnlyModelViewSet):
    queryset = Job.objects.all()
    serializer_class = MonthSerializer
    
    
    def list(self, request, *args, **kwargs):
        month = self.request.query_params['month']
        
        return super().list(request, *args, **kwargs)
    