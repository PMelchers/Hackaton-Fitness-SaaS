# Testplan — Registratie → Abonnement → Cursus-flow

**Scope:** integratie-/acceptatietest van de hoofd-flow: account aanmaken, inloggen,
abonnement kiezen, cursus in-/uitschrijven. Uitgevoerd met Django's `TestCase` +
test-`Client` (geen mocks, echte testdatabase) — geen losstaande unit-tests van
losse functies.

## Flow onder test
1. Registreren (`POST /register/`) → maakt `User`, `UserInfo`, `Customer` en een
   lege `Subscription` aan, logt automatisch in.
2. Inloggen (`POST /login/`) via e-mail (`EmailBackend`).
3. Abonnement kiezen (`POST /abonnement`) → koppelt `SubscriptionType` aan de
   klant, optioneel `addendum` = cursussen toegestaan.
4. Abonnement resetten (`GET /abonnement/reset`).
5. Cursus inschrijven/uitschrijven (`POST /cursussen/inschrijven/<id>/`,
   `POST /cursussen/uitschrijven/<id>/`).

## Happy-path gevallen
- Registratie → user/customer/subscription bestaan, sessie is ingelogd.
- Inloggen met juiste e-mail/wachtwoord.
- Abonnement kiezen (met en zonder addendum).
- Reset abonnement geeft schone `Subscription`.
- Inschrijven verlaagt beschikbaarheid en koppelt klant aan cursus.
- Uitschrijven verhoogt beschikbaarheid en ontkoppelt klant.

## Abuse-/randgevallen
- Dubbele gebruikersnaam / dubbel e-mailadres (case-insensitive).
- Zwak wachtwoord (Django password validators).
- Verplicht veld ontbreekt bij registratie.
- Verkeerd wachtwoord / onbekend e-mailadres bij inloggen.
- Niet-ingelogde gebruiker op `home`, `/abonnement`, cursus-endpoints → moet
  redirecten/afwijzen, nooit content lekken.
- `GET` op endpoints die `POST` vereisen (`logout`, cursus in-/uitschrijven) →
  moet 405 geven, niet de actie uitvoeren.
- Ongeldig/niet-bestaand `plan`-id bij abonnement kiezen.
- Ontbrekend `plan`-veld bij abonnement kiezen.
- Twee keer inschrijven voor dezelfde cursus (moet idempotent zijn, niet dubbel
  aftrekken).
- Inschrijven bij volle cursus (`availability <= 0`).
- Inschrijven zonder dat abonnement cursussen toestaat.
- Uitschrijven terwijl niet ingeschreven.
- Inschrijven voor niet-bestaande cursus → 404.

## Testcode
- `SAAS/accounts/tests.py` — registratie- en loginflow (9 tests).
- `SAAS/subscriptions/tests.py` — abonnement kiezen/resetten (7 tests).
- `SAAS/courses/tests.py` — cursus in-/uitschrijven (9 tests).

## Uitvoeren
```
cd SAAS
python manage.py test accounts subscriptions courses
```
