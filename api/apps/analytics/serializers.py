from email.policy import default
from rest_framework import serializers


class AnalyticsUserWorklogsSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    patronomic = serializers.CharField()
    total_worklogs = serializers.DecimalField(max_digits=100, decimal_places=2)


class AnalyticsJobsSerializer(serializers.Serializer):
    status = serializers.CharField()
    count = serializers.IntegerField(default=0)
