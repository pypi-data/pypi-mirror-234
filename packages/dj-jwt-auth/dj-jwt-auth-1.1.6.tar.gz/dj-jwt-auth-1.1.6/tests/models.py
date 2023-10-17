from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    kc_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    modified_timestamp = models.DateTimeField(auto_now=True)
