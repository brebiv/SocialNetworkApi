from django.urls import path
from . import views

urlpatterns = [
    path('user_list/', views.user_list, name='user_list'),
    path('register/', views.register_user, name='register_user'),
]