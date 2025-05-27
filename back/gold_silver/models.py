# gold_silver/models.py
from django.db import models

# Create your models here.
class GoldPrice(models.Model):
    date = models.DateTimeField()
    close = models.FloatField()
    volume = models.FloatField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()

class SilverPrice(models.Model):
    date = models.DateTimeField()
    close = models.FloatField()
    volume = models.FloatField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
