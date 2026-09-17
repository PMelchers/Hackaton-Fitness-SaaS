from django.urls import path

from .views import enroll_view, withdraw_view

urlpatterns = [
    path("cursussen/inschrijven/<int:course_id>/", enroll_view, name="course_enroll"),
    path("cursussen/uitschrijven/<int:course_id>/", withdraw_view, name="course_withdraw"),
]
