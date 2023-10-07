"""General API Views"""
from typing import Any
from django.urls import reverse
from django.views.generic import TemplateView
from kfsd.apps.frontend.views.permissions.base import PermissionView
from kfsd.apps.frontend.permissions.signin import SignInRequired
from kfsd.apps.frontend.permissions.staff import IsStaff
from kfsd.apps.frontend.permissions.active import IsActive
from kfsd.apps.frontend.permissions.email import SignUpEmailVerified


class APIDocsView(PermissionView, TemplateView):
    """Show browser view based on rapi-doc"""

    permission_classes = [SignInRequired, IsActive, SignUpEmailVerified, IsStaff]
    permission_classes_neg = []

    template_name = "v1/docs/browser.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        path = self.request.build_absolute_uri(
            reverse(
                "schema-api",
            )
        )
        return super().get_context_data(path=path, **kwargs)
