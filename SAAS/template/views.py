from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from courses.models import Course


@login_required
def home(request):
    customer = getattr(request.user, "customer", None)
    courses = Course.objects.select_related("type").all()
    trainer_courses = courses.filter(type__name__iexact="Persoonlijke trainer")
    regular_courses = courses.exclude(pk__in=trainer_courses.values("pk"))
    enrolled_ids = set(customer.course_set.values_list("id", flat=True)) if customer else set()

    context = {
        "customer": customer,
        "regular_courses": regular_courses,
        "trainer_courses": trainer_courses,
        "enrolled_ids": enrolled_ids,
    }
    return render(request, "template.html", context)
