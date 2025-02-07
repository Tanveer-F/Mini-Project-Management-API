from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or getattr(request.user, 'role', None) == 'admin'

class IsProjectCreator(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
      return obj.creator == request.user


class IsAdminOrTaskUpdater(permissions.BasePermission):
    def has_permission(self, request, view):
        #Ensure the user is authenticated before checking object-level permissions."""
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Check if user has permission on the specific object."""
        # Admins have full access
        if getattr(request.user, 'role', None) == 'admin':
            return True

        # For PATCH or PUT requests, if the task is assigned to the requesting member...
        if request.method in ['PATCH', 'PUT'] and obj.assigned_to == request.user:
            allowed_fields = {'status'}
            if hasattr(request, 'data') and set(request.data.keys()).issubset(allowed_fields):
                return True

        return False
