from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import UserSerializer, RegistrationSerializer, PostCreateSerializer, PostSerializer
from .models import Post, Like
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


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


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticatedOrReadOnly])
def create_post(request):
    if request.method == "GET":
        qs = Post.objects.all()
        serializer = PostSerializer(qs, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    elif request.method == "POST":
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
    user = request.user
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        data['message'] = "Post Does Not Exist"
        return Response(data, status.HTTP_404_NOT_FOUND)

    try:
        like = Like.objects.get(post=post, user=user)
        data['message'] = "You already liked this post"
    except Like.DoesNotExist:
        print("Like does not exist")
        print(user)
        print(post)
        like = Like.objects.create(user=user, post=post)
        like.save()
        data['message'] = "Post liked successfuly"
    return Response(data, status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def dislike_post(request, post_id):
    data = {}
    user = request.user

    try:
        post = Post.objects.get(pk=post_id)
        like = Like.objects.get(user=user, post=post)
    except Post.DoesNotExist:
        data['message'] = "Post doest not exist"
        return Response(data, status.HTTP_404_NOT_FOUND)
    except Like.DoesNotExist:
        data['message'] = "You didn't like this post"
        return Response(data, status.HTTP_404_NOT_FOUND)
    else:
        like.delete()
        data['message'] = "Like deleted successfuly"
        return Response(data, status.HTTP_204_NO_CONTENT)
