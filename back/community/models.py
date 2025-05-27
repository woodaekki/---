# community/models.py

from django.db import models
from django.conf import settings


# Create your models here.
class Community(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    category = models.IntegerField(default=2)  # 기본값은 자유게시판 (2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Review(models.Model):
    community = models.ForeignKey(
        Community, on_delete=models.CASCADE, related_name='reviews'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FixedCommunity(models.Model):
    user = models.TextField()
    title = models.CharField(max_length=100)
    content = models.TextField()
    category = models.IntegerField()