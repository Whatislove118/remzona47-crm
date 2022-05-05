from rest_framework import serializers

from api.apps.work_process.models import Favour, Job
from rest_auth.serializers import UserDetailsSerializer


class JobCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"
        read_only_fields = ["id", "status"]
        extra_kwargs = {"master": {"required": False}}


class JobDetailsSerializer(JobCreateSerializer):
    master = UserDetailsSerializer(many=False, read_only=True)

    class Meta(JobCreateSerializer.Meta):
        model = Job
        fields = "__all__"
        read_only_fields = ["id", "status"]


class FavourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favour
        fields = "__all__"
        read_only_fields = ["id"]
