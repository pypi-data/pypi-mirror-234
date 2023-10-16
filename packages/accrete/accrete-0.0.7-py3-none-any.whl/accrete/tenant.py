import contextvars
import logging
from django.apps import apps

_logger = logging.getLogger(__name__)

tenant_contextvar = contextvars.ContextVar('tenant', default=None)
member_contextvar = contextvars.ContextVar('member', default=None)


def set_tenant(tenant):
    tenant_contextvar.set(tenant)


def get_tenant():
    return tenant_contextvar.get()


def set_member(member):
    tenant = member.tenant if member is not None else None
    member_contextvar.set(member)
    tenant_contextvar.set(tenant)


def get_member():
    return member_contextvar.get()


def tenant_iterator():
    for tenant in apps.get_model('accrete', 'Tenant').objects.all():
        set_tenant(tenant)
        yield tenant


class Unscoped:

    def __init__(self, tenant):
        self.tenant = tenant

    def __enter__(self):
        if self.tenant is None:
            _logger.warning(
                'Entering unscoped context manager with tenant already set to None!'
            )
        set_tenant(None)

    def __exit__(self, exc_type, exc_val, exc_tb):
        set_tenant(self.tenant)
