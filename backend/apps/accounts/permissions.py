from rest_framework.permissions import BasePermission

from apps.accounts.constants import UserRole


class IsOrganizationMember(BasePermission):
    message = "You must belong to an organization."

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and getattr(user, "organization_id", None)
        )


class IsOrganizationAdmin(BasePermission):
    message = "Admin role required."

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and user.role == UserRole.ADMIN
        )


class IsOperator(BasePermission):
    message = "Operator role required."

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and user.role == UserRole.OPERATOR
        )


class IsReviewer(BasePermission):
    message = "Reviewer role required."

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and user.role == UserRole.REVIEWER
        )


class IsOperatorOrAdmin(BasePermission):
    message = "Operator or admin role required."

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and user.role in {UserRole.OPERATOR, UserRole.ADMIN}
        )


class CanViewOrganizationRequests(BasePermission):
    """Any authenticated member of an organization may view requests."""

    message = "Authentication required."

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and getattr(user, "organization_id", None)
        )
