from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import UserSerializer, RegistrationSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.
@api_view(["GET"])
def user_list(request):
    qs = User.objects.all()
    serializer = UserSerializer(qs, many=True)
    return Response(serializer.data)

