import logging
from django.db import transaction
from django.db.models import F

from .models import Sequence

_logger = logging.getLogger(__name__)


def get_nextval(tenant, name, create_if_none=True):
    with transaction.atomic():
        seq = Sequence.objects.filter(
            tenant=tenant.id, name=name
        ).select_for_update().first()

        if seq is None and not create_if_none:
            raise AttributeError(f'No sequence for {name} found!')
        elif seq is None:
            seq = Sequence(name=name, tenant=tenant)
            seq.save()

        nextval = seq.nextval
        seq.nextval = F('nextval') + seq.step
        seq.save()

    return nextval
