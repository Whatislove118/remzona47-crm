from rest_framework import serializers
from api.apps.work_process.serializers import JobSerializer


class DaySerializer(serializers.Serializer):
    jobs = JobSerializer(many=True, read_only=True)
    day_number = serializers.IntegerField()
    day_name = serializers.CharField()
    
    def validate(self, data):
        
        pass

class MonthSerializer(serializers.Serializer):
    month_number = serializers.IntegerField()
    month_name = serializers.CharField()
    days = DaySerializer(many=True, read_only=True)
    
    def validate(self, data):
        
        pass
    

    

