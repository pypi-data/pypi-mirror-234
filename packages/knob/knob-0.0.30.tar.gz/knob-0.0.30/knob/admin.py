# -*- coding:utf-8 -*-
from django.utils.html import format_html


__all__ = ['rich_tag']


def rich_tag(text, color=None, bold=False, italic=False, hint=None, link=None, tag='span'):
    opts = {
        "text": text,
        "color": "color: {};".format(color) if color else "",
        "tag": tag if link is None else 'a',
        "bold": " font-weight: bold;" if bold else "",
        "italic": " font-style: italic;" if italic else "",
        "link": link,
    }

    if link is not None:
        link_tmpl = ' href="{link}"'
    else:
        link_tmpl = ''

    if hint:
        opts['hint'] = hint
        tmpl = u'<{tag} style="{color}{bold}{italic}" title="{hint}"' + link_tmpl + '>{text}</{tag}>'
    else:
        tmpl = u'<{tag} style="{color}{bold}{italic}"' + link_tmpl + '>{text}</{tag}>'

    return format_html(tmpl, **opts)
