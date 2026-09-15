from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from customer.models import Customer

from .models import Subscription, SubscriptionType

PLAN_ACCESS = {
    "1x per week": 1,
    "2x per week": 2,
    "onbeperkt": -1,
}


@login_required
def request_subscription(request):
    if request.method == "POST":
        plan_name = request.POST.get("plan", "2x per week")
        addendum = request.POST.get("addendum") == "on"

        subscription_type, _ = SubscriptionType.objects.get_or_create(
            name=plan_name,
            defaults={"price": 0, "access": PLAN_ACCESS.get(plan_name, 0)},
        )
        subscription = Subscription.objects.create(
            name=f"{plan_name} abonnement",
            type=subscription_type,
            cources_allowed=addendum,
        )

        customer = getattr(request.user, "customer", None)
        if customer:
            customer.subscription = subscription
            customer.save()
        else:
            Customer.objects.create(user=request.user, subscription=subscription)

        return redirect("home")

    context = {"selected_plan": "2x per week", "addendum": True}
    return render(request, "subscriptions/request.html", context)
