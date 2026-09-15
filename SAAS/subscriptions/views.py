from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .models import Subscription, SubscriptionType

# Create your views here.
@login_required
def request_subscription(request):
    return render(request, "request.html")

@login_required
def process_request(request):
    user = None

    if not request.user.is_authenticated:
        raise PermissionDenied()

    user = request.user
    
    if user:
        subscriptions = SubscriptionType.objects.all()
        return render(request, "test.html", context={"request": request.POST["plan"]})