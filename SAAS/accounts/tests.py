from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from customer.models import Customer

User = get_user_model()

VALID_REGISTER_DATA = {
    "username": "janjansen",
    "first_name": "Jan",
    "insert": "",
    "last_name": "Jansen",
    "email": "jan@example.com",
    "street_name": "Teststraat",
    "house_number": "12",
    "postcode": "1234AB",
    "password": "correcthorsebatterystaple",
}


class RegisterFlowTests(TestCase):
    def test_register_creates_user_customer_subscription_and_logs_in(self):
        response = self.client.post(reverse("register"), VALID_REGISTER_DATA, follow=True)

        self.assertRedirects(response, reverse("home"))
        user = User.objects.get(username="janjansen")
        self.assertTrue(user.check_password(VALID_REGISTER_DATA["password"]))
        self.assertTrue(hasattr(user, "info"))
        customer = Customer.objects.get(user=user)
        self.assertIsNotNone(customer.subscription)
        self.assertEqual(int(self.client.session["_auth_user_id"]), user.pk)

    def test_register_duplicate_username_rejected(self):
        User.objects.create_user(username="janjansen", email="other@example.com", password="x")

        response = self.client.post(reverse("register"), VALID_REGISTER_DATA)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "username", "Deze gebruikersnaam is al in gebruik.")
        self.assertEqual(User.objects.filter(email="jan@example.com").count(), 0)

    def test_register_duplicate_email_case_insensitive_rejected(self):
        User.objects.create_user(username="other", email="JAN@example.com", password="x")

        response = self.client.post(reverse("register"), VALID_REGISTER_DATA)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "email", "Dit e-mailadres is al in gebruik.")

    def test_register_weak_password_rejected(self):
        data = {**VALID_REGISTER_DATA, "password": "12345678"}

        response = self.client.post(reverse("register"), data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="janjansen").exists())

    def test_register_missing_required_field_rejected(self):
        data = {**VALID_REGISTER_DATA}
        del data["street_name"]

        response = self.client.post(reverse("register"), data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="janjansen").exists())


class LoginFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="janjansen", email="jan@example.com", password="correcthorsebatterystaple"
        )

    def test_login_with_correct_credentials_succeeds(self):
        response = self.client.post(
            reverse("login"),
            {"email": "jan@example.com", "password": "correcthorsebatterystaple"},
            follow=True,
        )

        self.assertRedirects(response, reverse("home"))
        self.assertEqual(int(self.client.session["_auth_user_id"]), self.user.pk)

    def test_login_with_wrong_password_rejected(self):
        response = self.client.post(
            reverse("login"), {"email": "jan@example.com", "password": "wrongpassword"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_login_with_unknown_email_rejected(self):
        response = self.client.post(
            reverse("login"), {"email": "unknown@example.com", "password": "whatever123"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_home_requires_login(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_logout_requires_post(self):
        self.client.login(username="janjansen", password="correcthorsebatterystaple")

        response = self.client.get(reverse("logout"))

        self.assertEqual(response.status_code, 405)
