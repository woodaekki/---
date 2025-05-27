from django.db import models

class CustomerRecord(models.Model):
    age = models.PositiveIntegerField()
    income = models.PositiveIntegerField()
    jobs = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    product_type = models.CharField(max_length=10)  # '예금' or '적금'
    bank_name = models.CharField(max_length=50)
    product_name = models.CharField(max_length=100)
