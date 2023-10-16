from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _

ACCRETE_UI_ACTIONS_TEMPLATE = getattr(
    settings, 'ACCRETE_UI_ACTIONS_TEMPLATE',
    'ui/partials/actions.html'
)
