from django.db import models
from django.core.exceptions import ValidationError
from company.models import Company
from product.messages import ERROR_MESSAGES
import datetime


class Product(models.Model):
    name = models.CharField(max_length=25)
    model = models.CharField(max_length=100)
    market_launch_date = models.DateField()
    company = models.ManyToManyField(Company, related_name='products')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'model'], name='unique_product'),
        ]

    def clean(self):
        first_company_creation_date = Company.objects.get(level__exact=0).creation_date.date()
        current_date = datetime.date.today()
        if self.market_launch_date > current_date:
            raise ValidationError({'market_launch_date': ERROR_MESSAGES['gt_current_date']})
        elif self.market_launch_date < first_company_creation_date:
            raise ValidationError(
                {'market_launch_date': ERROR_MESSAGES['gt_first_company_date'].format(first_company_creation_date)},
            )

    def __str__(self):
        return f"{self.name}, {self.model}"
