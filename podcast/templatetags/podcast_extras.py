from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def podcast_url(name):
    return getattr(settings, name, "")