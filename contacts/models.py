from django.db import models
from company.models import Company


class Address(models.Model):
    country = models.CharField(max_length=60)
    city = models.CharField(max_length=150)
    street = models.CharField(max_length=150, blank=True, default='')
    house_number = models.CharField(max_length=50)

    class Meta:
        unique_together = [('country', 'city', 'street', 'house_number')]
        verbose_name_plural = 'addresses'

    def __str__(self):
        full_address = [field for field in (self.country, self.city, self.street, self.house_number) if field]
        return ", ".join(full_address)


class Email(models.Model):
    description = models.CharField(max_length=150, blank=True, default='main email')
    email = models.EmailField()

    class Meta:
        unique_together = [('email', 'description')]

    def __str__(self):
        return f'{self.email} - {self.description}'


class Contacts(models.Model):
    email = models.ManyToManyField(Email)
    address = models.ForeignKey(Address, on_delete=models.PROTECT)
    company = models.OneToOneField(Company, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.company} contacts"

    class Meta:
        verbose_name = 'contact'
