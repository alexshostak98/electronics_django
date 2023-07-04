from django.contrib.auth.models import User
from rest_framework import serializers


class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email']
        extra_kwargs = {
            "url": {"view_name": "api:user-detail"}
        }


class EmployeeDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
