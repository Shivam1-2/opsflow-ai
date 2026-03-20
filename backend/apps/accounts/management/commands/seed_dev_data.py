from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.accounts.constants import UserRole
from apps.organizations.models import Organization

User = get_user_model()

DEV_PASSWORD = "dev-password-change-me"


class Command(BaseCommand):
    help = "Create development organization and sample users (development only)."

    def handle(self, *args, **options):
        org, _ = Organization.objects.get_or_create(
            slug="acme-dev",
            defaults={"name": "Acme Development"},
        )
        users = [
            ("admin@acme.dev", UserRole.ADMIN),
            ("operator@acme.dev", UserRole.OPERATOR),
            ("reviewer@acme.dev", UserRole.REVIEWER),
        ]
        for email, role in users:
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "organization": org,
                    "role": role,
                    "is_active": True,
                },
            )
            if created:
                user.set_password(DEV_PASSWORD)
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Created {email} ({role})"))
            else:
                self.stdout.write(f"Exists {email}")

        self.stdout.write(
            self.style.WARNING(
                f"Development password for seeded users: {DEV_PASSWORD} "
                "(never use in production)."
            )
        )
