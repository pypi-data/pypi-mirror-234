from django import template

register = template.Library()

@register.filter
def get_url(obj, attr):
    return f"{getattr(obj, attr)}_url"
