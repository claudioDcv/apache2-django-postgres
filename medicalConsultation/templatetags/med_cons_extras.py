from django import template

register = template.Library()


@register.simple_tag
def uppercase(value):
    """Removes all values of arg from the given string"""
    return value.upper()


@register.simple_tag
def crr_order_by(value, value2):
    """Removes all values of arg from the given string"""
    value3 = '-'+value2
    if value == value2:
        value = value3
    else:
        if value == value3:
            value = value2

    if value != value2 and value != value3:
        value = value2
    return value
