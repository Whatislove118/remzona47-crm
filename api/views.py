from rest_framework.viewsets import ModelViewSet
from rest_framework import serializers
from core import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import Group
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model


User = get_user_model



@api_view(['GET'])
def health(request):
    if request.method == 'GET':
        return Response({'detail': 'ok'})