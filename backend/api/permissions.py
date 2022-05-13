from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    '''Кастомный пермишен,
    который позволяет автору редактировать его контент.
    '''
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS or (
                request.user.is_authenticated
                and (obj.author == request.user or request.user.is_superuser)
            )
        )
