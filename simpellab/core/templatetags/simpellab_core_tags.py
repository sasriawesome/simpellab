import re
from decimal import Decimal

from django import template
from django.conf import settings
from django.utils.formats import number_format
from django.contrib import admin
from simpellab.utils.text import number_to_text_id

register = template.Library()


class CustomRequest:
    def __init__(self, user):
        self.user = user


@register.filter(is_safe=True)
def money(value, use_l10n=True):
    """
    Convert an integer to a string containing commas every three digits.
    For example, 3000 becomes '3,000' and 45000 becomes '45,000'.
    """
    if settings.USE_L10N and use_l10n:
        try:
            if not isinstance(value, (float, Decimal)):
                value = int(value)
        except (TypeError, ValueError):
            return money(value, False)
        else:
            return number_format(value, decimal_pos=2, force_grouping=True)
    orig = str(value)
    new = re.sub(r"^(-?\d+)(\d{3})", r'\g<1>,\g<2>', orig)
    if orig == new:
        return new
    else:
        return money(new, use_l10n)


@register.filter(is_safe=True)
def point(value):
    """
    Convert an integer to a string containing commas every three digits.
    For example, 3000 becomes '3,000' and 45000 becomes '45,000'.
    """
    return "{:20,.2f}".format(value)


@register.simple_tag(name='sum')
def sum(value1, value2):
    value1 = value1 or 0
    value2 = value2 or 0
    return (float(value1) + float(value2))


@register.filter(name='percentof')
def percentof(value1, value2):
    """ Return Percent Of """
    v1 = value1 or 0
    v2 = value2 or 1
    return (v1 / v2) * 100


@register.filter(name='number_to_text')
def number_to_text(value):
    number = value or 0
    return number_to_text_id(int(number))
