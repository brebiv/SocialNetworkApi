from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token


# Create your models here.
class Post(models.Model):

    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="posts")
    likes = models.IntegerField(verbose_name='likes', default=0)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, unique=False)
    date_liked = models.DateTimeField(auto_now_add=True)


# Create token when user registers
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
