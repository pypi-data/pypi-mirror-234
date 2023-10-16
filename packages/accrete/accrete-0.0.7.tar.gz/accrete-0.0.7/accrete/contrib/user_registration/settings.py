from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _

USER_REGISTRATION_MAIL_FROM_NAME = getattr(
    settings, 'USER_REGISTRATION_MAIL_FROM_NAME',
    False
)

USER_REGISTRATION_TEMPLATE_NAME = getattr(
    settings, 'USER_REGISTRATION_TEMPLATE_NAME',
    'user_registration/mail_templates/confirmation_mail.html'
)

USER_REGISTRATION_MAIL_SUBJECT = getattr(
    settings, 'USER_REGISTRATION_MAIL_SUBJECT',
    _('Registration Confirmation')
)

USER_REGISTRATION_ALLOWED = getattr(
    settings, 'USER_REGISTRATION_ALLOWED', False
)

if not USER_REGISTRATION_MAIL_FROM_NAME:
    raise ImproperlyConfigured(
        'Setting "USER_REGISTRATION_MAIL_FROM_NAME" missing.\n'
        'User Registration won\'t work. Set it or remove '
        'the app "user_registration" from INSTALLED_APPS and your urls.'
    )
