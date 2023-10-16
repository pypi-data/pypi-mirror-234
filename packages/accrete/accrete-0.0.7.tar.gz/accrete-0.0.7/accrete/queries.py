import logging
from accrete import models
from accrete.tenant import get_tenant

_logger = logging.getLogger(__name__)

def is_member(tenant, user):
    return tenant.members.filter(user=user, is_active=True).exists()

def members_for_current_tenant():
    tenant = get_tenant()
    return tenant and tenant.members or models.Member.objects.none()

def all_tenants():
    return models.Tenant.objects.all()