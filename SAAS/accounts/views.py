from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import LoginForm, RegisterForm
from .models import UserInfo
from customer.models import Customer
from subscriptions.models import Subscription

User = get_user_model()


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = authenticate(
            request,
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password"],
        )
        if user is not None:
            login(request, user)
            return redirect("home")
        messages.error(request, "Ongeldige inloggegevens.")

    return render(request, "accounts/login.html", {"form": form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        user = User.objects.create_user(
            username=data["username"],
            email=data["email"],
            password=data["password"],
            first_name=data["first_name"],
            last_name=data["last_name"],
        )
        UserInfo.objects.create(
            user=user,
            insert=data["insert"],
            street_name=data["street_name"],
            house_number=data["house_number"],
            postcode=data["postcode"],
        )

        Customer.objects.create(
            user=user,
            subscription=Subscription.objects.create()
        )
        login(request, user, backend="accounts.backends.EmailBackend")
        return redirect("home")

    return render(request, "accounts/register.html", {"form": form})


@require_POST
def logout_view(request):
    logout(request)
    return redirect("login")
