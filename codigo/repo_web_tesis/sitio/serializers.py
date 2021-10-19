from django.core import serializers
from django.db.models import Model
import json


def list_properties(cls):
    if not hasattr(cls, '__dict__'):
        return []

    return [k for k, v in dict(cls.__dict__).items() if type(v) is property]

class PropBaseSerializer(serializers.base.Serializer):
    """
    Custom serializer class which enables us to specify a subset
    of model class properties (as well as fields)
    """

    def serialize(self, queryset, **options):
        self.ignored_props = options.pop('ignored_props', dict())
        self.selected_props = options.pop('props', '__all__')
        return super().serialize(queryset, **options)

    def serialize_property(self, obj):
        model = type(obj)

        model_props = self.selected_props or '__all__'

        if model_props == '__all__':
            model_props = list_properties(model)
        
        for prop in model_props:
            if prop not in self.ignored_props:
                if issubclass(type(getattr(obj, prop)), Model):
                    self.handle_model(obj, prop)
                    
                elif prop in model_props and hasattr(model, prop) and type(getattr(model, prop)) == property:
                    self.handle_prop(obj, prop)

    def handle_prop(self, obj, prop):
        try:
            self._current[prop] = getattr(obj, prop)
        except:
            pass
    
    def handle_model(self, obj, prop):
        options = getattr(obj, prop + '_options', dict())

        value = getattr(obj, prop)
        many = hasattr(value, 'all') or hasattr(value, '__len__')

        serialized = json.loads(ModelJsonSerializer().serialize(value if many else [value], **options))

        self._current[prop] = serialized if many else serialized[0]

    def end_object(self, obj):
        self.serialize_property(obj)
        super().end_object(obj)


class ModelPythonSerializer(PropBaseSerializer, serializers.python.Serializer):
    pass


class ModelJsonSerializer(ModelPythonSerializer, serializers.json.Serializer):
    pass
