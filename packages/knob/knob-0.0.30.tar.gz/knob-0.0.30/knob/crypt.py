# -*- coding:utf-8 -*-

import six
from Crypto.Cipher import AES
import base64


__all__ = ['encrypt', 'decrypt']


def _pad_key(key):
    if len(key) > 32:
        return key[:32]
    elif len(key) > 24:
        return key.ljust(32)
    elif len(key) > 16:
        return key.ljust(24)
    else:
        return key.ljust(16)


def encrypt(msg, key=None, url_safe=False):
    if not key:
        return msg
    else:
        key = _pad_key(key)
        if not isinstance(key, bytes):
            key = key.encode('utf-8')

    msg = (msg + '$').encode('utf-8')
    padded_msg = msg.ljust((len(msg) // 16 + 1) * 16)
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted = cipher.encrypt(padded_msg)
    if url_safe:
        encoded = base64.b64encode(encrypted, altchars=b'-_')
    else:
        encoded = base64.b64encode(encrypted)
    return encoded.decode('utf-8')


def decrypt(encoded, key=None, url_safe=False):
    if not key:
        if isinstance(encoded, bytes):
            return encoded.decode('utf-8')
        else:
            return encoded
    else:
        key = _pad_key(key)
        if not isinstance(key, bytes):
            key = key.encode('utf-8')

    cipher = AES.new(key, AES.MODE_ECB)
    if url_safe:
        decoded = base64.b64decode(encoded, altchars=b'-_')
    else:
        decoded = base64.b64decode(encoded)
    padded_msg = cipher.decrypt(decoded)
    msg = padded_msg.rstrip()
    msg = msg.decode('utf-8')
    msg = msg[:-1]
    return msg


