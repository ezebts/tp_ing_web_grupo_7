from django import template
from django.db.models import Model
from sitio.serializers import ModelJsonSerializer
from django.utils.safestring import SafeString

register = template.Library()


@register.filter(name='field_type')
def field_type(field):
    return field.field.widget.__class__.__name__


@register.filter(name='field_attrs')
def field_attrs(field):
    return field.field.widget.attrs


@register.filter(name='json')
def json(data, **options):
    single = isinstance(data, Model)

    if single:
        data = [data]

    result = ModelJsonSerializer().serialize(data, **options)

    if single:
        result = result[1:len(result) - 1]

    return SafeString(result)


@register.filter(name='get_key')
def get_key(d, k):
    return d.get(k, '') if d else ''
