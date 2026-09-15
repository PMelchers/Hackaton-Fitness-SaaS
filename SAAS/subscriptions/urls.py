from django.urls import path
from .views import request_subscription, process_request

urlpatterns = [
    path("abonnement", request_subscription, name="subscription_request"),
    path("abonnement/aanvragen/", process_request, name="process_request")
]
