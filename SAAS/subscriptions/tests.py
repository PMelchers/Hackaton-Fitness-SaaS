from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from customer.models import Customer
from subscriptions.models import Subscription, SubscriptionType

User = get_user_model()


class SubscriptionFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="jan", email="jan@example.com", password="pw12345678!")
        self.customer = Customer.objects.create(user=self.user, subscription=Subscription.objects.create())
        self.plan = SubscriptionType.objects.create(name="Basic", price=9.99, access=1)
        self.client.login(username="jan", password="pw12345678!")

    def test_request_subscription_requires_login(self):
        self.client.logout()

        response = self.client.get(reverse("subscription_request"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_choose_plan_updates_customer_subscription(self):
        response = self.client.post(reverse("subscription_request"), {"plan": self.plan.id})

        self.assertEqual(response.status_code, 200)
        self.customer.subscription.refresh_from_db()
        self.assertEqual(self.customer.subscription.type, self.plan)
        self.assertFalse(self.customer.subscription.cources_allowed)

    def test_choose_plan_with_addendum_allows_courses(self):
        response = self.client.post(
            reverse("subscription_request"), {"plan": self.plan.id, "addendum": "on"}
        )

        self.assertEqual(response.status_code, 200)
        self.customer.subscription.refresh_from_db()
        self.assertTrue(self.customer.subscription.cources_allowed)

    def test_choose_nonexistent_plan_raises_server_error(self):
        # Abuse case: a tampered/invalid plan id is not validated and blows up
        # the view with an unhandled DoesNotExist instead of a 4xx response.
        with self.assertRaises(SubscriptionType.DoesNotExist):
            self.client.post(reverse("subscription_request"), {"plan": 99999})

    def test_missing_plan_field_raises_server_error(self):
        # Abuse case: posting without the "plan" field crashes with a KeyError
        # instead of returning a validation error to the client.
        with self.assertRaises(KeyError):
            self.client.post(reverse("subscription_request"), {})

    def test_reset_subscription_creates_fresh_subscription(self):
        self.customer.subscription.type = self.plan
        self.customer.subscription.cources_allowed = True
        self.customer.subscription.save()
        old_subscription_id = self.customer.subscription.id

        response = self.client.get(reverse("subscription_reset"))

        self.assertRedirects(response, reverse("subscription_request"))
        self.customer.refresh_from_db()
        self.assertNotEqual(self.customer.subscription.id, old_subscription_id)
        self.assertIsNone(self.customer.subscription.type)
        self.assertFalse(self.customer.subscription.cources_allowed)
