from functools import wraps

from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.views import login_required
from django.core.exceptions import ImproperlyConfigured

TENANT_NOT_SET_URL = settings.ACCRETE_TENANT_NOT_SET_URL

def tenant_required(
        tenant_not_set_url: str = None,
        redirect_field_name: str = None,
        login_url: str = None
):
    def decorator(f):
        @wraps(f)
        @login_required(
            redirect_field_name=redirect_field_name,
            login_url=login_url
        )
        def _wrapped_view(request, *args, **kwargs):
            tenant = request.tenant
            if not tenant:
                url = tenant_not_set_url or TENANT_NOT_SET_URL
                if not url:
                    raise ImproperlyConfigured(
                        f'Redirect URL not set. '
                        f'Define settings.ACCRETE_TENANT_NOT_SET_URL or pass '
                        f'the redirect URL to the tenant_required decorator.'
                    )
                return redirect(url)
            return f(request, *args, **kwargs)
        return _wrapped_view
    return decorator
