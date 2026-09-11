from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Wachtwoord", widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(label="gebruikers naam", max_length=150)
    first_name = forms.CharField(label="voornaam", max_length=150)
    insert = forms.CharField(label="tussen voegsel", max_length=50, required=False)
    last_name = forms.CharField(label="achternaam", max_length=150)
    email = forms.EmailField(label="email")
    street_name = forms.CharField(label="straatnaam", max_length=255)
    house_number = forms.IntegerField(label="huisnummer")
    postcode = forms.CharField(label="postcode", max_length=10)
    password = forms.CharField(label="wachtwoord", widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Deze gebruikersnaam is al in gebruik.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Dit e-mailadres is al in gebruik.")
        return email

    def clean_password(self):
        password = self.cleaned_data["password"]
        validate_password(password)
        return password
