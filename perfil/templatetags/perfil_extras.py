from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def divide(value, arg):
    try:
        return float(value) / float(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0

@register.simple_tag(takes_context=True)
def can_save_more(context):
    user = context['user']
    if user.is_authenticated and hasattr(user, 'perfil'):
        return user.perfil.can_save_more_products()
    return False