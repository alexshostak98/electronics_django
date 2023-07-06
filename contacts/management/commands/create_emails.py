import random
from string import ascii_letters, digits
from django.core.management.base import BaseCommand
from contacts.constants import ALL_DATA_ROWS, EMAILS_DESCRIPTIONS, EMAIL_DOMAIN
from contacts.models import Email


class Command(BaseCommand):
    help = 'Fill the email table with test data'

    def handle(self, *args, **options):
        emails = []
        population = ascii_letters + digits + '_'
        for _ in range(ALL_DATA_ROWS):
            email = ''.join(random.choices(population=population, k=7)) + EMAIL_DOMAIN
            description = random.choice(EMAILS_DESCRIPTIONS)
            email_obj = Email(email=email, description=description)
            emails.append(email_obj)
        Email.objects.bulk_create(emails)
        self.stdout.write(self.style.SUCCESS(f'{len(emails)} row was successfully added to table'))
