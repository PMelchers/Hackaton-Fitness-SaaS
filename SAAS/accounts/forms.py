from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

inputStyling = "bg-white border-[#e5e7eb] border-[2px] border-solid rounded-[20px] h-[40px] w-[200px]"

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"class": inputStyling, "placeholder" : "Email..."}))
    password = forms.CharField(label="Wachtwoord", widget=forms.PasswordInput(attrs={"class": inputStyling, "placeholder" : "Wachtwoord..."}))

class RegisterForm(forms.Form):
    username = forms.CharField(label="gebruikers naam", max_length=150, widget=forms.TextInput(attrs={"class": inputStyling, "placeholder" : "Gebruikers naam..."}))
    first_name = forms.CharField(label="voornaam", max_length=150, widget=forms.TextInput(attrs={"class": inputStyling, "placeholder" : "Voornaam..."}))
    insert = forms.CharField(label="tussen voegsel", max_length=50, required=False, widget=forms.TextInput(attrs={"class": inputStyling, "placeholder" : "Tussen voegsel..."}))
    last_name = forms.CharField(label="achternaam", max_length=150, widget=forms.TextInput(attrs={"class": inputStyling, "placeholder" : "Achternaam..."}))
    email = forms.EmailField(label="email", widget=forms.EmailInput(attrs={"class": inputStyling, "placeholder" : "Email..."}))
    street_name = forms.CharField(label="straatnaam", max_length=255, widget=forms.TextInput(attrs={"class": inputStyling, "placeholder" : "Straatnaam..."}))
    house_number = forms.IntegerField(label="huisnummer", widget=forms.NumberInput(attrs={"class": inputStyling, "placeholder" : "Huisnummer..."}))
    postcode = forms.CharField(label="postcode", max_length=10, widget=forms.TextInput(attrs={"class": inputStyling, "placeholder" : "Postcode..."}))
    password = forms.CharField(label="wachtwoord", widget=forms.PasswordInput(attrs={"class": inputStyling, "placeholder" : "Wachtwoord..."}))

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
