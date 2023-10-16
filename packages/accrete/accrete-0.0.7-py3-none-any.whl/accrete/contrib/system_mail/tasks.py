import logging
from celery import shared_task

from django.core import mail
from django.db import transaction
from django.utils.html import strip_tags

from .models import SystemMail

_logger = logging.getLogger(__name__)


@shared_task()
def run_mail_queue():
    with transaction.atomic():
        _logger.info('Starting System Mail Queue')
        mails_to_send = SystemMail.objects.filter(
            sent=False).select_for_update()
        for email in mails_to_send:
            _logger.info(f'Sending mail: {email}')
            try:
                msg = strip_tags(email.body)
                mail.send_mail(
                    email.subject, msg, email.from_name,
                    email.to_addr.split(','), html_message=email.body
                )
            except Exception as e:
                error_str = str(e)
                _logger.error(f'Failed to send system mail\n{error_str}')
                email.error = error_str
                email.save()
                continue

            email.sent = True
            email.error = None
            email.save()
