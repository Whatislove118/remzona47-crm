from rest_framework import serializers
from api.work_process.models import Job

class JobSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ['id', 'status'] 
        