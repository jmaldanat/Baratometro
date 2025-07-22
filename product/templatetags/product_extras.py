from django import template

register = template.Library()

@register.filter
def cop(value):
    try:
        value = float(value)
        return "${:,.0f} COP".format(value).replace(",", ".")
    except (ValueError, TypeError):
        return "$0 COP"