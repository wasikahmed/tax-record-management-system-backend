from rest_framework import permissions


class IsTaxPayer(permissions.BasePermission):
    # Allows access only to users in the 'Taxpayers' group
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.groups.filter(name='Taxpayers').exists()
            or request.user.is_superuser
        )
    

class IsTaxOfficer(permissions.BasePermission):
    # Allows access only to users in the 'Officers' group
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.groups.filter(name='Officers').exists()
            or request.user.is_superuser
        )


class IsOwnerOrOfficer(permissions.BasePermission):
    # Object-level permission
    # Officers can access anyone's data
    # Taxpayers can only access their own data
    def has_object_permission(self, request, view, obj):
        # Superusers and Officers get full access
        if request.user.is_superuser or request.user.groups.filter(name='Officers').exists():
            return True
        
        # Taxpayers can only access their own objects
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        if hasattr(obj, 'taxpayer'):
            return obj.taxpayer.user == request.user
        
        return False
        
