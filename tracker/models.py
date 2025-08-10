from django.db import models

# Create your models here.

class CurrentBalance(models.Model):
    income = models.FloatField(default=0)   # Total income earned (never decreases)
    balance = models.FloatField(default=0)  

class TrackingHistory(models.Model):
    amount = models.FloatField()
    description = models.CharField(max_length=200)
    expense_type = models.CharField(choices=[("CREDIT","CREDIT"),("DEBIT","DEBIT")], max_length=10)
    created_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    income = models.ForeignKey(CurrentBalance, on_delete=models.CASCADE)