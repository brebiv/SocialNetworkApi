from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('users/', views.user_list, name='user_list'),
    path('register/', views.register_user, name='register_user'),
    path('login/', obtain_auth_token, name='login'),
]