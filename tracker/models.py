from django.db import models
from django.contrib.auth.models import User
from django.contrib import messages

# Create your models here.

class CurrentBalance(models.Model):
    income = models.FloatField(default=0)   # Total income earned (never decreases)
    balance = models.FloatField(default=0)  
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
class TrackingHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.FloatField()
    description = models.CharField(max_length=200)
    expense_type = models.CharField(choices=[("CREDIT","CREDIT"),("DEBIT","DEBIT")], max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)  # creation timestamp
    income = models.ForeignKey(CurrentBalance, on_delete=models.CASCADE)
