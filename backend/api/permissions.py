from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Кастомный пермишен, который позволяет автору редактировать его контент.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user
