from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('users/', views.user_list, name='user_list'),
    path('register/', views.register_user, name='register_user'),
    path('login/', obtain_auth_token, name='login'),
    path('posts/', views.create_post, name='create_post'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('dislike/<int:post_id>/', views.dislike_post, name='dislike_post'),
    path('analitics/', views.like_analitics, name='likes_analitics'),
]