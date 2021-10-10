from haystack import indexes
from sitio.models import Publicacion


class PublicacionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    titulo = indexes.CharField(model_attr='titulo')
    carrera = indexes.IntegerField(model_attr='carrera')
    fecha_publicacion = indexes.DateTimeField(model_attr='fecha_publicacion')

    def get_model(self):
        return Publicacion

    """TODO: Cambiar estado a 'publicada' """
    def index_queryset(self, using=None):
        """Queremos que se indexen todas las publicaciones que se hayan Publicado"""
        return self.get_model().objects.filter(estado='en_revision')
