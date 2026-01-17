from rest_framework import permissions

class IsTaxPayer(permissions.BasePermission):
    """Allows access if the user has a TaxPayer profile."""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return hasattr(request.user, 'taxpayerprofile') or request.user.is_superuser


class IsTaxOfficer(permissions.BasePermission):
    """Allows access if the user has a TaxOfficer profile."""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return hasattr(request.user, 'taxofficerprofile') or request.user.is_superuser


class IsOwnerOrOfficer(permissions.BasePermission):
    """
    - Officers/Admins: Can view/edit any object.
    - Taxpayers: Can only view/edit objects that belong to them.
    """
    def has_object_permission(self, request, view, obj):
        # Superusers and Officers get full access
        if request.user.is_superuser or hasattr(request.user, 'taxofficerprofile'):
            return True

        # Check if the user is the 'owner' of the object
        
        # Object is the Profile itself (TaxPayerProfile)
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        # Object is linked to a Taxpayer (TaxReturn, SupportTicket)
        if hasattr(obj, 'taxpayer'):
            return obj.taxpayer.user == request.user

        # Payment (linked via TaxReturn)
        if hasattr(obj, 'tax_return'):
            return obj.tax_return.taxpayer.user == request.user
            
        return False