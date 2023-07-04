from django.contrib.auth.models import User
from rest_framework import viewsets
from api.employee import serializers
from rest_framework import mixins


class EmployeeViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = User.objects.all()
    serializer_class = serializers.EmployeeSerializer
    action_serializers = {
        'retrieve': serializers.EmployeeDetailSerializer,
    }

    def get_serializer_class(self):
        return self.action_serializers.get(self.action, self.serializer_class)
