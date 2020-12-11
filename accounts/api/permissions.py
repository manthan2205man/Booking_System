from rest_framework.permissions import BasePermission, SAFE_METHODS


class BookingOwnerOnly(BasePermission):
    message = 'You Are Not Owner of this Booking. You can\'t change or delete it Bro.'

    def  has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.customer == request.user

class ToolOwnerOnly(BasePermission):
    message = 'You Are Not Owner of this Tool. You can\'t change or delete it Bro.'

    def  has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.owner == request.user