from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils import timezone
from .serializers import UserSerializer, RegistrationSerializer, PostCreateSerializer, PostSerializer, LikeSerializer
from .models import Post, Like
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from django.core.exceptions import ValidationError
import datetime

from . import utils


# Create your views here.
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_list(request):
    utils.track_user(request.user)
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
        utils.track_user(request.user)
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
    utils.track_user(request.user)
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
    utils.track_user(request.user)
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

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def like_analitics(request):
    # analitics/?date_from=2020-02-02&date_to=2020-02-15
    data = {}
    try:
        date_from = request.GET['date_from']
        date_to = request.GET['date_to']
        likes = Like.objects.filter(date_liked__range=(date_from, date_to))
    except KeyError:
        data['message'] = "Wrong request"
        return Response(data, status.HTTP_400_BAD_REQUEST)
    except Post.DoesNotExist:
        data['message'] = "Not posts'he been liked in that period"
        return Response(data, status.HTTP_404_NOT_FOUND)
    except ValidationError:
        data['message'] = "Invalid format. It must be in YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]"
        return Response(data, status.HTTP_400_BAD_REQUEST)
    serializer = LikeSerializer(likes, many=True)
    return Response(serializer.data, status.HTTP_200_OK)