from collections import namedtuple
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.dispatch import Signal
from django.utils import timezone

from repo_web_tesis import helpers


def namedtuple_choices(nmtuple):
    return (
        (getattr(nmtuple, field), field.replace('_', ' '))
        for field in nmtuple._fields
    )


ESTADOS_USUARIO = namedtuple(
    'EstadosUsuario',
    'VERIFICADO NO_VERIFICADO BLOQUEADO_PERM BLOQUEADO_TEMP'
)(1, 2, 3, 4)


class UsuarioSignals(Signal):
    new = Signal()

    def send(self, *args, is_new=False, **kwargs):
        super().send(*args, is_new=is_new, **kwargs)

        if is_new:
            self.new.send(*args, **kwargs)


class UsuarioManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        superuser = super().create_superuser(username, email, password, **extra_fields)
        superuser.estado = ESTADOS_USUARIO.VERIFICADO
        superuser.save()
        return superuser


class Usuario(AbstractUser):
    """
    Usuario base del sitio
    """

    objects = UsuarioManager()

    on_created = UsuarioSignals()

    email = models.EmailField(blank=False, null=False, unique=True)

    estado = models.IntegerField(
        choices=namedtuple_choices(ESTADOS_USUARIO), default=ESTADOS_USUARIO.NO_VERIFICADO)

    imagen = models.ImageField(null=True, default=None)

    @property
    def verified(self):
        return self.estado == ESTADOS_USUARIO.VERIFICADO

    def send_email(self, subject, template, context={}):
        context['usuario'] = self
        helpers.send_email([self.email], subject, template, context=context)

    def save(self, *args, creation=False, **kwargs):
        """
        creation=True validará si es un nuevo usuario
        y enviará notificaciones relacionadas
        """

        is_new = creation and self.pk is None

        super().save(*args, **kwargs)

        self.on_created.send(sender=self.__class__,
                             is_new=is_new, usuario=self)


class Autor(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)

    @property
    def full_name(self):
        nombre = str(self.nombre).capitalize()
        apellido = str(self.apellido).capitalize()

        return f'{ nombre } { apellido }'


class Publicacion(models.Model):

    ESTADOS_PUBLICACION = (
        ('publicada','La publicación está activa'),
        ('borrador', 'La publicación está siendo escrita y no activa'),
        ('en_revision', 'La publicacion esta siendo evaluada por administradores'),
        ('bloqueada', 'La publicacion no está activa'),
    )


    estado = models.CharField(max_length=200, choices=ESTADOS_PUBLICACION, default='en_revision')
    usuario = models.ForeignKey('Usuario', on_delete=DO_NOTHING)
    autores = models.ManyToManyField(Autor)
    fecha_creacion = models.DateField(default=timezone.now)
    año_creacion = models.DateField(default=timezone.now)
    titulo = models.CharField(max_length=100)
    resumen = models.CharField(max_length=300)
    vistas = models.IntegerField(default=0)
    archivo = models.FileField(upload_to='', blank=True)
    imagen = models.FileField(upload_to='', blank=True)


class Comentario(models.Model):
    texto = models.CharField(max_length=100)
    archivo = models.FileField(upload_to='', blank=True)
    publicacion = models.ForeignKey(Publicacion, on_delete=CASCADE,)
