# -*- coding:utf-8 -*-

import os
import six
from django.conf import settings

__all__ = ['get_setting', 'set_setting', 'turn_on_debug', 'turn_off_debug', 'is_debug_on']

setting_pool = []
dynamic_setting = None

if 'constance' in settings.INSTALLED_APPS:
    try:
        from constance import config as constance_config
        setting_pool.append(constance_config)
        dynamic_setting = 'Constance'
    except ImportError:
        constance_config = None

setting_pool.append(settings)

_DEBUG = 'DEBUG_KNOB_SETTING' in os.environ
_DEBUG_SETTINGS_DICT = {}


def turn_on_debug():
    global _DEBUG
    _DEBUG = True


def turn_off_debug():
    global _DEBUG
    _DEBUG = False
    _DEBUG_SETTINGS_DICT.clear()


def is_debug_on():
    return _DEBUG


def get_setting(key, default=None):
    if is_debug_on() and key in _DEBUG_SETTINGS_DICT:
        return _DEBUG_SETTINGS_DICT[key]

    res = default
    for setting in setting_pool:
        if hasattr(setting, key):
            res = getattr(setting, key)
    return res


def set_setting(key, value):
    if is_debug_on():
        _DEBUG_SETTINGS_DICT[key] = value
    else:
        if dynamic_setting == 'Constance':
            setattr(constance_config, key, value)
        else:
            raise RuntimeError("No dynamic setting module installed.")
