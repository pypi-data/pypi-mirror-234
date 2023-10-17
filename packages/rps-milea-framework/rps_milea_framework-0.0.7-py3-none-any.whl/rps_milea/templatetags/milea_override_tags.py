from django.template import Library
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.contrib.admin.views.main import PAGE_VAR

register = Library()

@register.simple_tag
def milea_paginator_number(cl, i):
    """
    Generate an individual page index link in a paginated list.
    """
    if i == cl.paginator.ELLIPSIS:
        return format_html("{} ", cl.paginator.ELLIPSIS)
    else:
        return format_html(
            '<li class="page-item {}"><a class="page-link" href="{}"{}>{}</a></li>',
            'active' if i == cl.page_num else '',
            cl.get_query_string({PAGE_VAR: i}),
            mark_safe(' class="end"' if i == cl.paginator.num_pages else ""),
            i,
        )

@register.simple_tag
def setvar(val=None):
    return val
