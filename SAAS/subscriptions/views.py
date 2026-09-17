from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .models import Subscription, SubscriptionType
from customer.models import Customer

# Create your views here.
@login_required
def request_subscription(request):
    if request.method == "GET":
        return render(request, "request.html")
    elif request.method == "POST":
        user = request.user
        message = ""
        if user:
            customer = Customer.objects.get(user=user)
            chosen_subscription = SubscriptionType.objects.get(id=request.POST["plan"])
            customer.subscription.type = chosen_subscription
            message = f"Je hebt nu abonnement {chosen_subscription.name}"

            if request.POST.get("addendum"):
                customer.subscription.cources_allowed = True
                message += " met cursussen"
        
            customer.subscription.save()
            customer.save()
        
        return render(request, "request.html", context={"message": message})

@login_required
def reset_subscription(request):
    user = request.user

    if user:
        customer = Customer.objects.get(user=user)
        customer.subscription = Subscription.objects.create()
        customer.subscription.save()

    return redirect("subscription_request")
