from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from api.company import serializers
from api.company.filters import CompanyFilter
from company.models import Company
from contacts.models import Email
from company.messages import SUCCESS_MESSAGES, ERROR_MESSAGES
from company.tasks import send_email_with_qr_code


class CompanyViewSet(viewsets.ModelViewSet):
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
        companies_with_above_average_debt = queryset.filter(debt_to_supplier__gt=average_debt['avg_debt'])
        return Response(self.get_serializer(companies_with_above_average_debt, many=True).data)

    @action(methods=['get'], detail=True, url_path='send-qrcode-to-email', name='Send QR code to email')
    def send_qr_code_with_company_contacts_to_email(self, request, pk):
        company = self.get_object()
        try:
            contacts = company.contacts
        except ObjectDoesNotExist:
            return Response({'status', ERROR_MESSAGES['has_not_email']})
        emails = [email_data.email for email_data in Email.objects.filter(contacts=contacts.pk)]
        contacts_text = f"{contacts.address}\n{', '.join(emails)}"
        send_email_with_qr_code.delay(contacts_text, company.name, emails)
        return Response({'status': SUCCESS_MESSAGES['send_qr_code_to_email']})
