from random import choice, choices, randint
from django.core.management.base import BaseCommand
from company.models import Company
from contacts.models import Contacts, Address, Email


class Command(BaseCommand):
    help = 'Fill the contacts table with test data'
    companies = Company.objects.all()
    addresses = Address.objects.all()
    emails = Email.objects.all()
    all_contacts = []

    def handle(self, *args, **options):
        for company in self.companies:
            address = choice(self.addresses)
            email = choices(self.emails, k=randint(1, 3))
            contacts = Contacts(address=address, company=company)
            contacts.save()
            contacts.email.set(email)
            self.all_contacts.append(contacts)
        for email in self.emails:
            email.contacts_set.set(choices(self.all_contacts, k=randint(1, 3)))
        self.stdout.write(self.style.SUCCESS(f'{len(self.all_contacts)} row was successfully added to table'))
