from django import template
import time

register = template.Library()


@register.filter
def epoch_to_date(value):
    return time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.localtime(value))
