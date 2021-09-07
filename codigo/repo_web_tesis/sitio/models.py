from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
from django.dispatch import Signal




from repo_web_tesis import helpers

# Create your models here.
class Usuario(AbstractUser):
    """
    Usuario base del sitio
    """

    on_created = Signal()

    def send_email(self, subject, template, context={}):
        context['user'] = self
        helpers.send_email([self.email], subject, template, context)

    def save(self, *args, creation=False, **kwargs):
        is_commited = kwargs.get('commit', False)
        is_new = creation and is_commited and self.pk is None
        super(Usuario, self).save(*args, **kwargs)
        self.on_created.send(sender=self.__class__, is_new=is_new)



class Autor(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    

class Publicacion(models.Model):
    autores = models.ManyToManyField(Autor) # Un autor tiene muchas publicaciones y una publicacion muchos autores
    fecha_creacion = models.DateField()
    titulo = models.CharField(max_length=100)
    resumen = models.CharField(max_length=300)
    vistas = models.IntegerField(default=0)
    archivo = models.FileField(upload_to='')
    imagen = models.FileField(upload_to='')


class Comentario(models.Model):
    texto = models.CharField(max_length=100)
    archivo = models.FileField(upload_to='', blank=True)
    publicacion = models.ForeignKey(Publicacion, on_delete=CASCADE,)