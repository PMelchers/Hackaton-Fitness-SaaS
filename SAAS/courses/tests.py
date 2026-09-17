from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from courses.models import Course, CourseType
from customer.models import Customer
from subscriptions.models import Subscription

User = get_user_model()


class CourseEnrollmentFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="jan", email="jan@example.com", password="pw12345678!")
        self.subscription = Subscription.objects.create(cources_allowed=True)
        self.customer = Customer.objects.create(user=self.user, subscription=self.subscription)
        course_type = CourseType.objects.create(name="Yoga", description="Rustige les")
        self.course = Course.objects.create(name="Yoga ochtend", type=course_type, availability=2)
        self.client.login(username="jan", password="pw12345678!")

    def test_enroll_requires_login(self):
        self.client.logout()

        response = self.client.post(reverse("course_enroll", args=[self.course.id]))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_enroll_requires_post(self):
        response = self.client.get(reverse("course_enroll", args=[self.course.id]))

        self.assertEqual(response.status_code, 405)

    def test_enroll_success_decrements_availability(self):
        response = self.client.post(reverse("course_enroll", args=[self.course.id]), follow=True)

        self.assertRedirects(response, reverse("home"))
        self.course.refresh_from_db()
        self.assertEqual(self.course.availability, 1)
        self.assertTrue(self.course.customers.filter(pk=self.customer.pk).exists())

    def test_enroll_blocked_when_subscription_disallows_courses(self):
        self.subscription.cources_allowed = False
        self.subscription.save()

        self.client.post(reverse("course_enroll", args=[self.course.id]))

        self.course.refresh_from_db()
        self.assertFalse(self.course.customers.filter(pk=self.customer.pk).exists())
        self.assertEqual(self.course.availability, 2)

    def test_enroll_twice_is_idempotent(self):
        self.client.post(reverse("course_enroll", args=[self.course.id]))

        self.client.post(reverse("course_enroll", args=[self.course.id]))

        self.course.refresh_from_db()
        self.assertEqual(self.course.availability, 1)
        self.assertEqual(self.course.customers.filter(pk=self.customer.pk).count(), 1)

    def test_enroll_blocked_when_course_full(self):
        self.course.availability = 0
        self.course.save()

        self.client.post(reverse("course_enroll", args=[self.course.id]))

        self.course.refresh_from_db()
        self.assertFalse(self.course.customers.filter(pk=self.customer.pk).exists())
        self.assertEqual(self.course.availability, 0)

    def test_enroll_unknown_course_returns_404(self):
        response = self.client.post(reverse("course_enroll", args=[99999]))

        self.assertEqual(response.status_code, 404)

    def test_withdraw_success_increments_availability(self):
        self.course.customers.add(self.customer)
        self.course.availability -= 1
        self.course.save()

        response = self.client.post(reverse("course_withdraw", args=[self.course.id]), follow=True)

        self.assertRedirects(response, reverse("home"))
        self.course.refresh_from_db()
        self.assertEqual(self.course.availability, 2)
        self.assertFalse(self.course.customers.filter(pk=self.customer.pk).exists())

    def test_withdraw_when_not_enrolled_leaves_availability_unchanged(self):
        response = self.client.post(reverse("course_withdraw", args=[self.course.id]), follow=True)

        self.assertRedirects(response, reverse("home"))
        self.course.refresh_from_db()
        self.assertEqual(self.course.availability, 2)
