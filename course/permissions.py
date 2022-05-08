from rest_framework import permissions


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return request.method in permissions.SAFE_METHODS or request.user.is_staff or request.user.is_superuser


class IsCommentOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """

        if (request.method in permissions.SAFE_METHODS):
            return True

        return request.user == obj.owner_of_comment


class IsTeacherCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_teacher or request.user.is_staff or request.user.is_superuser)


class IsCourseOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """

        return bool(request.user and request.user.is_authenticated) and (request.user == obj.author)
