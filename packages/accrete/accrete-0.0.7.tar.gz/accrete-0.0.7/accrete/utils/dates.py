import calendar
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from django.utils import timezone


def current_year_start() -> datetime:
    now = timezone.now()
    first_day = now.replace(
        month=1, day=1, hour=0, minute=0, second=0, microsecond=0
    )
    # calendar.monthrange(date.year, date.month)[1]
    return first_day


def current_year_end() -> datetime:
    now = timezone.now()
    last_day = now.replace(
        month=12, day=31, hour=23, minute=59, second=59, microsecond=999999
    )
    return last_day


def current_month_start() -> datetime:
    now = timezone.now()
    monthrange = calendar.monthrange(now.year, now.month)
    first_day = now.replace(
        day=1, hour=0, minute=0, second=0, microsecond=0
    )
    return first_day

def current_month_end() -> datetime:
    now = timezone.now()
    monthrange = calendar.monthrange(now.year, now.month)
    last_day = now.replace(
        day=monthrange[1], hour=23, minute=59, second=59, microsecond=999999
    )
    return last_day