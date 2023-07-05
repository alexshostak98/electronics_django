from rest_framework import permissions

"""
нужно если используем отличные от дефолтных настройки AUTHENTICATION_BACKENDS
т.к. дефолтный AUTHENTICATION_BACKENDS = django.contrib.auth.backends.ModelBackend,
который по умолчанию проверяет активен ли пользователь при входе
"""


class IsActive(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_active
