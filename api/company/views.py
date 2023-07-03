from rest_framework.viewsets import ModelViewSet
from api.company.serializers import CompanySerializer, CompanyDetailSerializer, CreateUpdateCompanySerializer
from company.models import Company


class CompanyViewSet(ModelViewSet):
    serializer_class = CreateUpdateCompanySerializer
    queryset = Company.objects.all()
    action_serializers = {
        'retrieve': CompanyDetailSerializer,
        'list': CompanySerializer,
    }

    def get_serializer_class(self):
        return self.action_serializers.get(self.action, self.serializer_class)
