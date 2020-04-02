from django.shortcuts import render, get_object_or_404
from .serializers import UserSerializer
from django.contrib.auth import get_user_model, authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_jwt.serializers import JSONWebTokenSerializer

@api_view(["POST"])
def signup(request):
    serializer = UserSerializer(data=request.data)
    print(serializer)
    if serializer.is_valid(raise_exception=True):
        user = UserSerializer.create(get_user_model(), request.data)
        serializer = UserSerializer(user)
        print(serializer)
        return Response(serializer.data)
