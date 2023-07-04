from django_filters import rest_framework as filters
from rest_framework.filters import BaseFilterBackend


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
    # change_list_template =


class IsEmployeeFilterBackend(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        user = request.user
        if user.is_superuser:
            return queryset
        return queryset.filter(employees=user.id)
