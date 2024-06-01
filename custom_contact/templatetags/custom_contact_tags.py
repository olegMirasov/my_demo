from django import template

register = template.Library()


@register.filter
def keyvalue(dict_, key):
    return dict_.get(key)
