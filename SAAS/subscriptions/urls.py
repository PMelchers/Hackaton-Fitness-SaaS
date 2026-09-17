from django.urls import path
from .views import request_subscription, reset_subscription

urlpatterns = [
    path("abonnement", request_subscription, name="subscription_request"),
    path("abonnement/reset", reset_subscription, name="subscription_reset"),
]
