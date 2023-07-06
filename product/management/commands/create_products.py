from datetime import date, timedelta
from random import choice, choices, randint
from string import ascii_lowercase
from django.core.management.base import BaseCommand
from company.models import Company
from contacts.constants import ALL_DATA_ROWS
from product.constants import PRODUCT_NAMES, PRODUCT_TYPES
from product.models import Product


class Command(BaseCommand):
    help = 'Fill the product table with test data'
    current_date = date.today()
    companies = Company.objects.order_by('creation_date').all()
    earliest_date = companies.first().creation_date.date()
    all_rows = 5 * ALL_DATA_ROWS
    date_differ = current_date - earliest_date
    all_products = []

    def handle(self, *args, **options):
        for _ in range(self.all_rows):
            product_type = choice(PRODUCT_TYPES)
            name = choice(PRODUCT_NAMES)
            model_name = ''.join(choices(ascii_lowercase, k=randint(0, 10)))
            model = model_name + str(randint(50, 500))
            market_launch_date = self.earliest_date + timedelta(days=randint(0, self.date_differ.days))
            company = choices(self.companies, k=randint(0, 10))
            product = Product(
                product_type=product_type, name=name, model=model, market_launch_date=market_launch_date
            )
            product.save()
            self.all_products.append(product)
            product.company.set(company)
        for company in self.companies:
            company.products.set(choices(self.all_products, k=randint(10, 50)))
            company.save()
        self.stdout.write(self.style.SUCCESS(f'{len(self.all_products)} row was successfully added to table'))
