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
    
class Comentario(models.Model):
    texto = models.CharField(max_length=100)
    archivo = models.FileField()

class Publicacion(models.Model):
    autores = models.ManyToManyField(Autor) # Un autor tiene muchas publicaciones y una publicacion muchos autores
    comentarios = models.ForeignKey(Comentario, on_delete=CASCADE, null=True) # Una publicacion tiene muchos comentarios
    fecha_creacion = models.DateField()
    titulo = models.CharField(max_length=50)
    resumen = models.CharField(max_length=100)
    vistas = models.IntegerField(null=True)
    archivo = models.FileField(null=True)
    imagen = models.ImageField(null=True)


# Investigar clase Manager para administrar las instancias de todos las clases.


