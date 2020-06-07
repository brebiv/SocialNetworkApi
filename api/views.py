from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import UserSerializer, RegistrationSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token


# Create your views here.
@api_view(["GET"])
def user_list(request):
    qs = User.objects.all()
    serializer = UserSerializer(qs, many=True)
    return Response(serializer.data)

@api_view(["POST"])
def register_user(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        user = serializer.save()
        data['message'] = "User successfuly created!"
        data['token'] = Token.objects.get(user=user).key
        return Response(data, status.HTTP_201_CREATED)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
