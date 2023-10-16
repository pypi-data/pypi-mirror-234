# -*- coding:utf-8 -*-

__all__ = ['local_now', 'local_today', 'local_time']

import six
from django.utils import timezone
from dt_utils import T


def local_now():
    return timezone.now().astimezone(timezone.get_current_timezone())


def local_today():
    return local_now().date()


def local_time(raw_time):
    time = T(raw_time)
    if timezone.is_aware(time):
        return timezone.localtime(time)
    else:
        return timezone.make_aware(time)
