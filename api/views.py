from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response

User = get_user_model


@api_view(["GET"])
def health(request):
    if request.method == "GET":
        return Response({"detail": "ok"})
