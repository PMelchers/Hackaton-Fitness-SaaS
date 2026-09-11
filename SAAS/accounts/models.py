from django.conf import settings
from django.db import models


class UserInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="info")
    insert = models.CharField(max_length=50, blank=True)
    street_name = models.CharField(max_length=255)
    house_number = models.IntegerField()
    postcode = models.CharField(max_length=10)

    def __str__(self):
        return f"UserInfo({self.user.username})"
