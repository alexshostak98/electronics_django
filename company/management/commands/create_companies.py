from collections import defaultdict
from random import choice, uniform, choices, randint
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from company.constants import RANDOM_COMPANY_NAMES, MAX_COMPANIES_PER_EMPLOYEE
from company.models import Company
from contacts.constants import ALL_DATA_ROWS


class Command(BaseCommand):
    help = 'Fill the company table with test data'
    limit_employee = defaultdict(int)
    limit_staff = defaultdict(int)
    staff_ids = list(User.objects.filter(is_staff=True).values_list('id', flat=True))
    employee_ids = list(User.objects.filter(is_staff=False).values_list('id', flat=True))
    employee_count = randint(1, MAX_COMPANIES_PER_EMPLOYEE)
    available_suppliers = []
    company_types = Company.ELEMENT_TYPES

    def handle(self, *args, **options):
        for index, name in zip(range(ALL_DATA_ROWS), RANDOM_COMPANY_NAMES):
            self._check_employees_limit(self.limit_employee, self.employee_ids)
            self._check_employees_limit(self.limit_staff, self.staff_ids)
            staff_ids_per_company = choices(self.staff_ids, k=self.employee_count)
            employee_ids_per_company = choices(self.employee_ids, k=self.employee_count)
            employees = staff_ids_per_company + employee_ids_per_company
            if index:
                company_type = choice(self.company_types)[0]
                supplier = choice(self.available_suppliers)
                debt_to_supplier = round(uniform(0, 10000), 2)
            else:
                company_type = self.company_types.pop(0)[0]
                supplier = debt_to_supplier = None
            company = Company(
                name=name,
                company_type=company_type,
                supplier=supplier,
                debt_to_supplier=debt_to_supplier,
            )
            company.save()
            company.employees.set(employees)
            self.available_suppliers.append(company)
        self.stdout.write(self.style.SUCCESS('Rows was successfully added to table'))

    @staticmethod
    def _check_employees_limit(limit, available_ids):
        for employee_id, id_count in limit.items():
            if id_count < MAX_COMPANIES_PER_EMPLOYEE:
                limit[employee_id] += 1
            else:
                available_ids.remove(employee_id)
