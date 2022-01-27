from atexit import register
from django import template

register = template.Library()

@register.filter()
def split(value,key):
    return list(value.split(key))