from django.db import migrations

DROP_UNIQUE_SQL = """
CREATE TABLE "subscriptions_subscription__new" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" varchar NOT NULL,
    "cources_allowed" bool NOT NULL,
    "saldo" integer NOT NULL,
    "type_id" bigint NULL REFERENCES "subscriptions_subscriptiontype" ("id") DEFERRABLE INITIALLY DEFERRED
);
INSERT INTO "subscriptions_subscription__new" ("id", "name", "cources_allowed", "saldo", "type_id")
    SELECT "id", "name", "cources_allowed", "saldo", "type_id" FROM "subscriptions_subscription";
DROP TABLE "subscriptions_subscription";
ALTER TABLE "subscriptions_subscription__new" RENAME TO "subscriptions_subscription";
CREATE INDEX "subscriptions_subscription_type_id_idx" ON "subscriptions_subscription" ("type_id");
"""

RESTORE_UNIQUE_SQL = """
CREATE TABLE "subscriptions_subscription__new" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" varchar NOT NULL,
    "cources_allowed" bool NOT NULL,
    "saldo" integer NOT NULL,
    "type_id" bigint NULL UNIQUE REFERENCES "subscriptions_subscriptiontype" ("id") DEFERRABLE INITIALLY DEFERRED
);
INSERT INTO "subscriptions_subscription__new" ("id", "name", "cources_allowed", "saldo", "type_id")
    SELECT "id", "name", "cources_allowed", "saldo", "type_id" FROM "subscriptions_subscription";
DROP TABLE "subscriptions_subscription";
ALTER TABLE "subscriptions_subscription__new" RENAME TO "subscriptions_subscription";
"""


class Migration(migrations.Migration):

    dependencies = [
        ("subscriptions", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(DROP_UNIQUE_SQL, reverse_sql=RESTORE_UNIQUE_SQL),
    ]
