from rest_framework import permissions

"""
нужно если используем отличные от дефолтных настройки AUTHENTICATION_BACKENDS
т.к. дефолтный AUTHENTICATION_BACKENDS = django.contrib.auth.backends.ModelBackend,
который по умолчанию проверяет активен ли пользователь при входе
"""


class IsActive(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_active


class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.is_staff
