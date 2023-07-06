import datetime
from rest_framework import serializers
from company.models import Company
from product.models import Product
from product.messages import ERROR_MESSAGES


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['company']
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Product.objects.all(),
                fields=['name', 'model'],
            )
        ]

    def validate_market_launch_date(self, value):
        first_company_creation_date = Company.objects.get(supplier__isnull=True).creation_date.date()
        current_date = datetime.date.today()
        if value > current_date:
            raise serializers.ValidationError(ERROR_MESSAGES['gt_current_date'])
        elif value < first_company_creation_date:
            raise serializers.ValidationError(
                ERROR_MESSAGES['gt_first_company_date'].format(first_company_creation_date),
            )
        return value
