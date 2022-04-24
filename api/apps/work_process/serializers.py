from rest_framework import serializers

from api.apps.work_process.models import Job
from rest_auth.serializers import UserDetailsSerializer


class JobCreateSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"
        read_only_fields = ["id", "status"]


class JobDetailsSerializer(JobCreateSerilizer):
    master = UserDetailsSerializer(many=False, read_only=True)

    class Meta(JobCreateSerilizer.Meta):
        model = Job
        fields = "__all__"
        read_only_fields = ["id", "status"]
