from rest_framework import serializers

from api.apps.work_process.models import Favour, Job, Workplaces
from rest_auth.models import Position
from rest_auth.serializers import PositionSerializer, UserDetailsSerializer


class JobCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"
        read_only_fields = ["id", "status"]


class JobDetailsSerializer(JobCreateSerializer):
    master = UserDetailsSerializer(many=False, read_only=True)

    class Meta(JobCreateSerializer.Meta):
        model = Job
        fields = "__all__"
        read_only_fields = ["id", "status"]


class FavourCreateSerializer(serializers.ModelSerializer):
    positions = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Position.objects.all()
    )

    class Meta:
        model = Favour
        fields = "__all__"
        read_only_fields = ["id"]


class FavourDetailsSerializer(FavourCreateSerializer):
    positions = PositionSerializer(many=True, read_only=True)

    class Meta(FavourCreateSerializer.Meta):
        pass


class WorkplacesSerializer(serializers.ModelSerializer):
    available_date_ranges = serializers.ListField(required=False)

    class Meta:
        model = Workplaces
        fields = "__all__"
        read_only_fields = ["id", "available_date_ranges"]
