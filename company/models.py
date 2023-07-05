from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from company.messages import ERROR_MESSAGES


class Company(models.Model):
    FACTORY = 'FA'
    DISTRIBUTOR = 'DB'
    DEALERSHIP = 'DS'
    RETAIL = 'RT'
    INDIVIDUAL = 'IE'
    ELEMENT_TYPES = [
        (FACTORY, 'Factory'),
        (DISTRIBUTOR, 'Distributor'),
        (DEALERSHIP, 'Dealership'),
        (RETAIL, 'Retail'),
        (INDIVIDUAL, 'Individual'),
    ]
    name = models.CharField(max_length=50)
    company_type = models.CharField(max_length=50, choices=ELEMENT_TYPES)
    supplier = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)
    debt_to_supplier = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    employees = models.ManyToManyField(User, related_name='works')

    class Meta:
        verbose_name_plural = 'companies'
        constraints = [
            models.CheckConstraint(
                check=models.Q(debt_to_supplier__gte=0),
                name='positive_debt',
                violation_error_message=ERROR_MESSAGES['positive_debt'],
            )
        ]

    def _factory_type_validate(self):
        if self.debt_to_supplier is not None:
            raise ValidationError({'debt_to_supplier': ERROR_MESSAGES['wrong_factory_debt']})
        if self.supplier is not None:
            raise ValidationError({'supplier': ERROR_MESSAGES['factory_supplier']})

    def _other_types_validate(self):
        if self.supplier:
            if self.debt_to_supplier:
                if self.debt_to_supplier < 0:
                    raise ValidationError({'debt_to_supplier': ERROR_MESSAGES['positive_debt']})
            else:
                self.debt_to_supplier = 0
        else:
            raise ValidationError({'supplier': ERROR_MESSAGES['should_has_supplier']})

    def clean(self):
        if self.company_type == self.FACTORY:
            self._factory_type_validate()
        else:
            self._other_types_validate()

    def get_model_name(self):
        return self._meta.model_name

    def get_model_app_label(self):
        return self._meta.app_label

    def __str__(self):
        return f'{self.get_company_type_display()} - {self.name}'
