from django import template

register = template.Library()


@register.filter(name="replace")
def quotations(value, arg):
    return value.replace(arg, " ")
