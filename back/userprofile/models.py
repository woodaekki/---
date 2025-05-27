from django.db import models
from django.conf import settings
from finance.models import DepositProducts, SavingProducts  # 실제 모델 경로에 맞게 조정하세요

class UserProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField()
    nickname = models.CharField(max_length=15, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    asset = models.PositiveIntegerField(help_text="자산 (원 단위)", null=True, blank=True)
    salary = models.PositiveIntegerField(help_text="연봉 (원 단위)", null=True, blank=True)
    liked_deposits = models.ManyToManyField(DepositProducts, blank=True, related_name='liked_by_users')
    liked_savings = models.ManyToManyField(SavingProducts, blank=True, related_name='liked_by_users')
