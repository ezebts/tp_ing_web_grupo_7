from django.core import serializers


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
        self.selected_props = options.pop('props', '__all__')
        return super().serialize(queryset, **options)

    def serialize_property(self, obj):
        model = type(obj)

        model_props = self.selected_props

        if model_props == '__all__':
            model_props = list_properties(model)

        for prop in model_props:
            if hasattr(model, prop) and type(getattr(model, prop)) == property:
                self.handle_prop(obj, prop)

    def handle_prop(self, obj, prop):
        self._current[prop] = getattr(obj, prop)

    def end_object(self, obj):
        self.serialize_property(obj)
        super().end_object(obj)


class ModelPythonSerializer(PropBaseSerializer, serializers.python.Serializer):
    pass


class ModelJsonSerializer(ModelPythonSerializer, serializers.json.Serializer):
    pass
