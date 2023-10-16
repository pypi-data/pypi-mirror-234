from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect
from django.conf import settings


class TenantRequiredMixin(LoginRequiredMixin):

    tenant_missing_url = None
    member_access_groups = []
    member_not_authorized_url = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.tenant:
            return self.handle_no_tenant()
        if not request.user.is_staff:
            if self.member_access_groups and not self.member_has_access():
                return self.handle_member_not_authorized()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_tenant(self):
        return redirect(self.get_tenant_not_set_url())

    def get_tenant_not_set_url(self):
        tenant_not_set_url = (
                self.tenant_missing_url
                or settings.ACCRETE_TENANT_NOT_SET_URL
        )
        if not tenant_not_set_url:
            cls_name = self.__class__.__name__
            raise ImproperlyConfigured(
                f"{cls_name} is missing the tenant_not_set_url attribute. "
                f"Define {cls_name}.tenant_not_set_url, "
                f"settings.ACCRETE_TENANT_NOT_SET_URL, or override "
                f"{cls_name}.get_tenant_not_set_url()."
            )
        return tenant_not_set_url

    def member_has_access(self):
        return self.request.member.access_groups.filter(
            code__in=self.member_access_groups
        ).exists()

    def handle_member_not_authorized(self):
        return redirect(self.get_member_not_authorized_url())

    def get_member_not_authorized_url(self):
        url = (self.member_not_authorized_url
               or settings.TENANT_MEMBER_NOT_AUTHORIZED_URL)
        if not url:
            cls_name = self.__class__.__name__
            raise ImproperlyConfigured(
                f"{cls_name} is missing the member_not_authorized_url "
                f"attribute. Define {cls_name}.member_not_authorized_url, "
                f"settings.TENANT_MEMBER_NOT_AUTHORIZED_URL, or override "
                f"{cls_name}.get_member_not_authorized_url()."
            )
        return url
