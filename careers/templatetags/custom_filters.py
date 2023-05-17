from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
@register.filter
def strip_spaces(value):
    return value.strip()