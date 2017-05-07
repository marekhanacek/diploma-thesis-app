from rest_framework.permissions import BasePermission

from web.service.acl import can_user_access_offer


class IsActualUserLogged(BasePermission):
    def has_object_permission(self, request, view, user):
        return user == request.user


class CanUserAccessOffer(BasePermission):
    def has_object_permission(self, request, view, offer):
        return can_user_access_offer(request.user, offer)
