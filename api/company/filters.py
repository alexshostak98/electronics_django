from django_filters import rest_framework as filters


class CompanyFilter(filters.FilterSet):
    company_country = filters.CharFilter(
        label='Country name',
        field_name='contacts__address__country',
        lookup_expr='exact',
    )
    product_id = filters.NumberFilter(
        label='Product ID',
        field_name='products__id',
        lookup_expr='exact',
    )
