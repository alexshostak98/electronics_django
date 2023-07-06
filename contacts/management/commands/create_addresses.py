import random
from django.core.management.base import BaseCommand
from contacts.constants import CITIES, STREETS, ADDRESSES_PER_COUNTRY
from contacts.models import Address


class Command(BaseCommand):
    help = 'Fill the address table with test data'

    def handle(self, *args, **options):
        addresses = []
        for country, cities in CITIES.items():
            for _ in range(ADDRESSES_PER_COUNTRY):
                city = random.choice(cities)
                street = random.choice(STREETS)
                house_number = random.randint(1, 100)
                address = Address(country=country, city=city, street=street, house_number=house_number)
                addresses.append(address)
        Address.objects.bulk_create(addresses)
        self.stdout.write(self.style.SUCCESS(f'{len(addresses)} row was successfully added to table'))
