from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .models import Course


@login_required
@require_POST
def enroll_view(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    customer = getattr(request.user, "customer", None)

    if not customer or not customer.subscription.cources_allowed:
        messages.error(request, "Je abonnement staat geen cursussen toe.")
    elif course.customers.filter(pk=customer.pk).exists():
        messages.info(request, "Je bent al ingeschreven voor deze cursus.")
    elif course.availability <= 0:
        messages.error(request, "Deze cursus zit vol.")
    else:
        course.customers.add(customer)
        course.availability -= 1
        course.save()
        messages.success(request, f"Ingeschreven voor {course.name}.")

    return redirect("home")


@login_required
@require_POST
def withdraw_view(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    customer = getattr(request.user, "customer", None)

    if not customer or not course.customers.filter(pk=customer.pk).exists():
        messages.error(request, "Je bent niet ingeschreven voor deze cursus.")
    else:
        course.customers.remove(customer)
        course.availability += 1
        course.save()
        messages.success(request, f"Uitgeschreven voor {course.name}.")

    return redirect("home")
