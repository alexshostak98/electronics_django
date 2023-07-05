from rest_framework import serializers
from company.models import Company
from company.messages import ERROR_MESSAGES
from api.employee.serializers import EmployeeSerializer
from api.product.serializers import ProductSerializer


class CompanySerializer(serializers.ModelSerializer):
    supplier = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='api:company-detail',
    )

    class Meta:
        model = Company
        fields = ['pk', 'name', 'company_type', 'supplier', 'debt_to_supplier', 'creation_date', 'level']


class CompanyDetailSerializer(CompanySerializer):
    employees = EmployeeSerializer(many=True)
    products = ProductSerializer(many=True)

    class Meta:
        model = Company
        fields = [
            'pk',
            'name',
            'company_type',
            'supplier',
            'debt_to_supplier',
            'creation_date',
            'level',
            'products',
            'contacts',
            'employees',
        ]


class CreateUpdateCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['pk', 'name', 'company_type', 'supplier', 'debt_to_supplier', 'creation_date', 'level']
        read_only_fields = ['level', 'creation_date']

    def create(self, validated_data):
        if validated_data['company_type'] == 'FA':
            level = 0
        else:
            level = validated_data['supplier'].level + 1
            if not validated_data['debt_to_supplier']:
                validated_data['debt_to_supplier'] = 0
        creator_employee = self.context.get('request').user
        company = Company.objects.create(level=level, **validated_data)
        company.employees.set([creator_employee])
        return company

    def update(self, instance, validated_data):
        if instance.debt_to_supplier != validated_data['debt_to_supplier']:
            raise serializers.ValidationError('Updating the debt_to_supplier field is forbidden')
        else:
            for field_name, field_value in validated_data.items():
                if field_value:
                    instance.__setattr__(field_name, field_value)
            instance.save()
            return instance

    def validate(self, attrs):
        supplier = attrs['supplier']
        debt_to_supplier = attrs['debt_to_supplier']
        if attrs['company_type'] == 'FA':
            if debt_to_supplier is not None:
                raise serializers.ValidationError(ERROR_MESSAGES['wrong_factory_debt'])
            if supplier is not None:
                raise serializers.ValidationError(ERROR_MESSAGES['factory_supplier'])
        else:
            if supplier:
                if debt_to_supplier:
                    if debt_to_supplier < 0:
                        raise serializers.ValidationError(ERROR_MESSAGES['positive_debt'])
            else:
                raise serializers.ValidationError(ERROR_MESSAGES['should_has_supplier'])
        return attrs
