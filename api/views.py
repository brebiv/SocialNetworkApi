from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import UserSerializer, RegistrationSerializer, PostCreateSerializer
from .models import Post
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


# Create your views here.
@api_view(["GET"])
@permission_classes([IsAuthenticated])
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


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_post(request):
    serializer = PostCreateSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        post = serializer.save(author=request.user)
        data['message'] = "Post successfuly created!"
        return Response(data, status.HTTP_201_CREATED)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def like_post(request, post_id):
    data = {}
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        data['message'] = "Post Does Not Exist"
        return Response(data, status.HTTP_404_NOT_FOUND)

    post.likes += 1
    post.save()
    data['message'] = "Post liked successfuly"
    return Response(data, status.HTTP_200_OK)
