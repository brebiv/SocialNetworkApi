from django.contrib.auth.models import User
from django.utils import timezone
import datetime, pytz


def track_user(user: User):
    user.last_login = timezone.now()
    user.save()
