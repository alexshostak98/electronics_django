from csv import DictWriter
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from random_username.generate import generate_username
from contacts.constants import ALL_DATA_ROWS


class Command(BaseCommand):
    help = 'Fill the user table with test data about employees'

    def handle(self, *args, **options):
        required_amount = 3 * ALL_DATA_ROWS
        user_names = list(set(generate_username(required_amount + ALL_DATA_ROWS)))[:required_amount]
        employees = []
        employees_with_password = []
        for index, user_name in zip(range(required_amount), user_names):
            is_staff = False
            if index % 3:
                is_staff = True
            employee = User(username=''.join(user_name), is_staff=is_staff)
            password = User.objects.make_random_password()
            employee.set_password(password)
            employees.append(employee)
            employees_with_password.append({'user': user_name, 'password': password})
        User.objects.bulk_create(employees)
        self._write_employees_data_to_csv(employees_with_password)
        self.stdout.write(self.style.SUCCESS(f'{len(employees)} row was successfully added to table'))

    @staticmethod
    def _write_employees_data_to_csv(employees_data):
        with open('employees.csv', mode='w', encoding='UTF-8') as csvfile:
            writer = DictWriter(csvfile, fieldnames=('user', 'password'), restval='')
            writer.writeheader()
            writer.writerows(employees_data)
