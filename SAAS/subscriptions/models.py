from django.db import models

# Create your models here.
class SubscriptionType(models.Model):
    name = models.CharField()
    price = models.FloatField()
    access = models.IntegerField()

class Subscription(models.Model):
    type = models.ForeignKey(SubscriptionType, on_delete=models.CASCADE, related_name='type', null=True)
    cources_allowed = models.BooleanField(default=False)
    saldo = models.IntegerField(default=0)
