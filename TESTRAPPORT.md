# Testrapport — Registratie → Abonnement → Cursus-flow

**Datum:** 2026-09-17
**Omgeving:** lokale sqlite testdatabase, Django test runner
**Eindresultaat:** 25/25 tests geslaagd, na 3 bugfixes (zie hieronder)

## Verloop

**Eerste testrun: 9 geslaagd / 16 gefaald.** Alle 16 faalden op dezelfde
oorzaak: `Subscription.objects.create()` gaf een `IntegrityError` (`NOT NULL
constraint failed: subscriptions_subscription.name`). Het model had het
`name`-veld niet meer, maar de migratie om die kolom te verwijderen ontbrak —
bevestigd met `manage.py makemigrations --check`. Op een verse database (nieuwe
clone, CI, staging) crasht **registratie zelf**, want die roept deze functie
aan (`accounts/views.py: register_view`).

**Fix 1 — ontbrekende migratie.** `python manage.py makemigrations subscriptions`
+ `migrate` toegepast → `subscriptions/migrations/0003_remove_subscription_name_alter_subscription_id_and_more.py`.

**Tweede testrun: nieuwe blocker.** De homepage-template
(`template/templates/template.html:19`) verwees ook nog naar het verwijderde
veld: `{{ customer.subscription.type.name|default:customer.subscription.name }}`.
Zodra een net geregistreerde gebruiker (nog geen abonnementstype gekozen) de
homepage laadt, crasht de render met `VariableDoesNotExist` — de
`default`-filter vangt een ontbrekend attribuut in zijn eigen argument niet
stil af. **Dit brak de homepage voor elke nieuwe gebruiker direct na
registratie.**

**Fix 2 — template.** Regel aangepast naar
`{{ customer.subscription.type.name|default:"geen abonnement gekozen" }}`.

**Derde testrun: laatste bug.** `reset_subscription`
(`subscriptions/views.py`) wees een nieuwe `Subscription` toe aan
`customer.subscription`, maar sloeg `customer` zelf nooit op — de koppeling
kwam dus nooit in de database terecht en de reset had geen effect.

**Fix 3 — `customer.save()`** toegevoegd na het toewijzen van de nieuwe
subscription.

**Vierde testrun: 25/25 geslaagd.**

## Root cause

Alle drie de bugs zijn gevolgen van dezelfde onvolledige refactor: het
`name`-veld is uit `Subscription` gehaald zonder de migratie en de template
mee te nemen, en de reset-actie was nooit end-to-end getest. Losse
symptoombestrijding (alleen de migratie, of alleen de template) had de flow
nog steeds gebroken laten staan.

## Overige bevinding (niet gefixt, wel gedekt door test)

`request_subscription` (`subscriptions/views.py`) valideert het `plan`-veld
niet: een ontbrekend veld geeft een onafgevangen `KeyError`, een
ongeldig/niet-bestaand plan-id een onafgevangen `SubscriptionType.DoesNotExist`
— beide crashen de request (500) in plaats van een nette foutmelding te tonen.
Vastgelegd in `subscriptions/tests.py::test_missing_plan_field_raises_server_error`
en `::test_choose_nonexistent_plan_raises_server_error` (deze tests
verwachten en bevestigen de crash — ze falen pas zodra iemand de validatie
toevoegt, wat dan de gewenste volgende stap is).

## Testresultaten (25 tests)
- `accounts/tests.py` (9): registratie- en loginflow — alle geslaagd.
- `subscriptions/tests.py` (7): abonnement kiezen/resetten, incl. de twee
  crash-bevestigende abuse-tests hierboven — alle geslaagd.
- `courses/tests.py` (9): cursus in-/uitschrijven, capaciteit, autorisatie —
  alle geslaagd.

## Conclusie
De hoofd-flow (registreren → inloggen → abonnement kiezen → cursus
in-/uitschrijven) is na de drie fixes end-to-end functioneel en acceptatieklaar
op een verse database. Voor de release: los de ontbrekende inputvalidatie op
`request_subscription` op (`plan`-veld), en neem `python manage.py test` op in
CI zodat een volgende ontbrekende migratie of dangling template-referentie
automatisch opvalt.
