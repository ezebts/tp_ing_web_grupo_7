from collections import namedtuple
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.dispatch import Signal
from django.utils import timezone
from django.urls import reverse

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

CARRERAS = (
    (1, 'Ingenieria en informatica'),
    (2, 'Abogacia'),
    (3, 'Contaduria'),
    (4, 'Medios visuales')
)


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


class Publicaciones(models.Manager):
    def filtrar(self, año=None, carreras=[]):
        unactive_state = Publicacion.ESTADOS_PUBLICACION[2][0]

        publicaciones = self.exclude(estado=unactive_state)

        if año:
            publicaciones = publicaciones.filter(fecha_publicacion__year=año)

        if carreras:
            publicaciones = publicaciones.filter(carrera__in=carreras)

        return publicaciones.order_by('-fecha_publicacion')


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
    def imagen_url(self):
        if self.imagen:
            return self.imagen.url
        else:
            return None

    @property
    def perfil_url(self):
        return reverse('perfil_publico', kwargs={'pk': self.pk})

    @property
    def verified(self):
        return self.estado == ESTADOS_USUARIO.VERIFICADO

    @property
    def siguiendo(self):
        siguiendo=[]
        for sig in self.u_siguiendo.all():
            siguiendo.append(sig.usuario_siguiendo)

        return siguiendo
    
    @property
    def seguidores(self):
        seguidores=[]
        for sig in self.u_seguidores.all():
            seguidores.append(sig.usuario)
        
        return seguidores

    def seguir(self, usuario_perfil):
        '''
        Self es el usuario logueado en el sitio,
        Usuario_perfil es el usuario del cual
        estamos visitando el perfil, luego
        al que queremos seguir
        '''
        seguimiento = Seguimiento()
        seguimiento.usuario=self
        seguimiento.usuario_siguiendo=usuario_perfil    

        seguimiento.save()    

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

    def __str__(self):
        return self.full_name


class Publicacion(models.Model):

    objects = Publicaciones()

    ESTADOS_PUBLICACION = (
        ('publicada', 'La publicación está activa'),
        ('en_revision', 'La publicacion esta siendo evaluada por administradores'),
        ('bloqueada', 'La publicacion no está activa'),
    )

    estado = models.CharField(
        max_length=200, choices=ESTADOS_PUBLICACION, default='en_revision')
    usuario = models.ForeignKey(Usuario, on_delete=DO_NOTHING, related_name='publicaciones')
    autores = models.ManyToManyField(Autor)
    fecha_creacion = models.DateField(default=timezone.now)
    fecha_publicacion = models.DateField(default=timezone.now)
    carrera = models.IntegerField(choices=CARRERAS, default=1)
    titulo = models.CharField(max_length=100)
    resumen = models.CharField(max_length=300)
    vistas = models.IntegerField(default=0)
    archivo = models.FileField(upload_to='', null=False, blank=False)
    imagen = models.FileField(upload_to='', null=False, blank=False)

    def __str__(self):
        return self.titulo

    @property
    def año_publicacion(self):
        return self.fecha_publicacion.strftime("%Y")

    def registrar_visita(self, usuario):
        if usuario.pk != self.usuario.pk:
            self.vistas += 1
            self.save()


class Comentario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=DO_NOTHING, related_name='comentarios')
    texto = models.TextField(max_length=1000)
    archivo = models.FileField(upload_to='', blank=True)
    fecha_creacion = models.DateField(default=timezone.now)
    publicacion = models.ForeignKey(Publicacion, on_delete=CASCADE, related_name='comentarios')

    


class Seguimiento(models.Model):
    usuario = models.ForeignKey(
        Usuario, related_name="u_siguiendo", on_delete=DO_NOTHING)
    usuario_siguiendo = models.ForeignKey(
        Usuario, related_name="u_seguidores", on_delete=DO_NOTHING)
    fecha_seguimiento = models.DateField(auto_now_add=True)


