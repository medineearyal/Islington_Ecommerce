from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


class GroupRequiredMixin:
    group_required = None

    def dispatch(self, request, *args, **kwargs):
        if self.group_required and not request.user.groups.filter(name=self.group_required).exists():
            raise PermissionDenied("Only sellers are authorized to access this page.")

        return super().dispatch(request, *args, **kwargs)


class SellerIsVerifiedMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_verified_seller:
            raise PermissionDenied("You must be verified to access this page.")
        return super().dispatch(request, *args, **kwargs)

