from django import template
from django.utils.safestring import mark_safe
from django.conf import settings

register = template.Library()


@register.inclusion_tag('react/include.html')
def include_react(*args, **kwargs):
    config = getattr(settings, 'REACT', dict())
    return {
        'environment': config.get('ENVIRONMENT', 'development')
    }


@register.inclusion_tag('react/container.html')
def react_container(content='#content', mount='#content'):
    return {
        'mount_point_selector': mount,
        'content_selector': content
    }
