from django.urls import path

from .views import request_subscription

urlpatterns = [
    path("abonnement/aanvragen/", request_subscription, name="subscription_request"),
]
