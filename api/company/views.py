from django.db.models import Avg
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from api.company import serializers
from api.company.filters import CompanyFilter
from company.models import Company


class CompanyViewSet(ModelViewSet):
    serializer_class = serializers.CreateUpdateCompanySerializer
    queryset = Company.objects.all()
    action_serializers = {
        'retrieve': serializers.CompanyDetailSerializer,
        'list': serializers.CompanySerializer,
    }
    filterset_class = CompanyFilter

    def get_serializer_class(self):
        return self.action_serializers.get(self.action, self.serializer_class)

    @action(methods=['get'], detail=False, url_path='debt-above-average')
    def debt_above_average(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        average_debt = queryset.exclude(debt_to_supplier__isnull=True).aggregate(avg_debt=Avg('debt_to_supplier'))
        companies_with_above_average_debt = queryset.filter(debt_to_supplier__gt=average_debt["avg_debt"])
        return Response(self.get_serializer(companies_with_above_average_debt, many=True).data)
