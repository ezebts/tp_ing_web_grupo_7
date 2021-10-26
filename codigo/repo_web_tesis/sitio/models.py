from collections import namedtuple
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.dispatch import Signal
from django.utils import timezone
from django.urls import reverse
from django.conf import settings

from repo_web_tesis import helpers

from itertools import chain


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
    def filtrar(self, usuario=None, año=None, carreras=[]):
        unactive_state = Publicacion.ESTADOS_PUBLICACION[2][0]

        publicaciones = self.exclude(estado=unactive_state)

        if año:
            publicaciones = publicaciones.filter(fecha_publicacion__year=año)

        if carreras:
            publicaciones = publicaciones.filter(carrera__in=carreras)

        feed = (
            publicaciones
            .annotate(weight=models.Value(0, models.IntegerField()))
            .order_by('-fecha_publicacion'))

        if usuario:
            feed_seguidores = (
                publicaciones
                .filter(usuario__in=usuario.u_siguiendo.all().values('usuario_siguiendo'))
                .annotate(weight=models.Value(1, models.IntegerField())))

            already_included = models.Q(id__in=feed_seguidores.values('id'))

            feed_standard = feed.filter(~already_included)

            return sorted(
                chain(feed_seguidores, feed_standard),
                key=lambda publ: (publ.fecha_publicacion, publ.weight), reverse=True)

        return feed


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

    @ property
    def imagen_url(self):
        if self.imagen:
            return self.imagen.url
        else:
            return None

    @ property
    def perfil_url(self):
        return reverse('perfil_publico', kwargs={'pk': self.pk})

    @ property
    def verified(self):
        return self.estado == ESTADOS_USUARIO.VERIFICADO

    def get_siguiendo(self):
        query = self.u_siguiendo.all().order_by(
            'usuario_siguiendo__username', '-fecha_seguimiento')

        return [
            seguimiento.usuario_siguiendo for seguimiento in query
        ]

    def get_seguidores(self):
        query = self.u_seguidores.all().order_by(
            'usuario__username', '-fecha_seguimiento')

        return [
            seguimiento.usuario for seguimiento in query
        ]

    def seguir(self, usuario_perfil):
        '''
        Self es el usuario logueado en el sitio,
        Usuario_perfil es el usuario del cual
        estamos visitando el perfil, luego
        al que queremos seguir
        '''
        if not self.u_siguiendo.filter(id=usuario_perfil.pk).exists():
            seguimiento = Seguimiento()
            seguimiento.usuario = self
            seguimiento.usuario_siguiendo = usuario_perfil

            seguimiento.save()

    def dejar_de_seguir(self, usuario):
        seguimiento = self.u_siguiendo.get(usuario_siguiendo__id=usuario.pk)
        if seguimiento:
            seguimiento.delete()

    def notificar(self, notificacion):
        notificacion.usuario = self
        notificacion.save()

    def send_email(self, subject, template, context={}):
        context['usuario'] = self
        helpers.send_email([self.email], subject, template, context=context)

    def get_notificacion_exact(self, notificacion):
        result = notificacion

        nuev_com = getattr(notificacion, 'notificacion_nuevo_comentario')
        nuev_seg = getattr(notificacion, 'notificacion_nuevo_seguidor')
        nuev_publ = getattr(notificacion, 'notificacion_nueva_publicacion')

        if nuev_com:
            result = nuev_com
        elif nuev_seg:
            result = nuev_seg
        elif nuev_publ:
            result = nuev_publ

        return result

    def get_notificacion(self, pk):
        notificacion = self.notificaciones.get(pk=pk)

        if notificacion:
            notificacion = self.get_notificacion_exact(notificacion)

        return notificacion

    def get_notificaciones(self):
        query = self.notificaciones.order_by('-fecha_creacion')

        return [
            self.get_notificacion_exact(notif) for notif in query
        ]

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

    @ property
    def full_name(self):
        nombre = str(self.nombre).capitalize()
        apellido = str(self.apellido).capitalize()

        return f'{ nombre } { apellido }'

    def __str__(self):
        return self.full_name


class Publicacion(models.Model):

    on_created = Signal()
    objects = Publicaciones()

    ESTADOS_PUBLICACION = (
        ('publicada', 'La publicación está activa'),
        ('en_revision', 'La publicacion esta siendo evaluada por administradores'),
        ('bloqueada', 'La publicacion no está activa'),
    )

    estado = models.CharField(
        max_length=200, choices=ESTADOS_PUBLICACION, default='en_revision')
    usuario = models.ForeignKey(
        Usuario, on_delete=DO_NOTHING, related_name='publicaciones')
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

    @ property
    def año_publicacion(self):
        return self.fecha_publicacion.strftime("%Y")

    @property
    def detalle_url(self):
        return reverse('publicacion') + f'?id={self.pk}'

    def registrar_visita(self, usuario):
        if usuario.pk != self.usuario.pk:
            self.vistas += 1
            self.save()

    def get_comentarios(self, padre_id=None):
        return (
            Comentario.objects
            .filter(publicacion__pk=self.pk, padre__pk=padre_id)
            .order_by('fecha_creacion')
        )

    def get_comentario(self, comentario_id):
        return self.comentarios.get(pk=comentario_id)

    def comentar(self, usuario, comentario, padre=None, revision=None, responde=None):
        comentario = Comentario(
            usuario=usuario,
            texto=comentario,
            archivo=revision,
            fecha_creacion=timezone.now(),
            publicacion=self,
            padre=padre,
            responde=responde
        )

        comentario.save()

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new:
            self.on_created.send(self.__class__, publicacion=self)


class Comentario(models.Model):
    usuario = models.ForeignKey(
        Usuario, on_delete=DO_NOTHING, related_name='comentarios')
    texto = models.TextField(max_length=1000)
    archivo = models.FileField(upload_to='', blank=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    publicacion = models.ForeignKey(
        Publicacion, on_delete=CASCADE, related_name='comentarios')
    padre = models.ForeignKey(
        'Comentario', on_delete=CASCADE, related_name='comentarios', null=True)
    responde = models.ForeignKey(
        'Comentario', on_delete=CASCADE, related_name='respuestas', null=True)

    on_created = Signal()

    @ property
    def responde_a_comentario(self):
        return self.responde

    @ property
    def autor(self):
        return self.usuario

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new:
            self.on_created.send(self.__class__, comentario=self)


class Seguimiento(models.Model):
    usuario = models.ForeignKey(
        Usuario, related_name="u_seguidores", on_delete=DO_NOTHING)
    usuario_siguiendo = models.ForeignKey(
        Usuario, related_name="u_siguiendo", on_delete=DO_NOTHING)
    fecha_seguimiento = models.DateField(auto_now_add=True)

    on_created = Signal()

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new:
            self.on_created.send(self.__class__, seguimiento=self)


class Notificacion(models.Model):
    on_created = Signal()

    notificacion_settings = 'Notificacion'

    usuario = models.ForeignKey(
        Usuario, related_name="notificaciones", on_delete=CASCADE)

    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_lectura = models.DateField(null=True)

    def get_text(self, element):
        config = settings.NOTIFICACIONES.get(self.get_settings(), dict())
        template = config.get(element)

        if not template:
            return

        context = self.get_context()
        context['notificacion'] = self

        return helpers.render_template(template, context=context)

    def get_context(self):
        return dict()

    def get_settings(self):
        return self.notificacion_settings

    @ property
    def mensaje(self):
        return self.get_text('mensaje')

    @property
    def link(self):
        return None

    @ property
    def cabecera(self):
        return self.get_text('cabecera')

    @ property
    def vista(self):
        return self.fecha_lectura is not None

    def marcar_como_vista(self):
        self.fecha_lectura = timezone.now()
        self.save()

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new:
            self.on_created.send(sender=self.__class__, notificacion=self)


class NotificacionNuevoComentario(Notificacion):
    notificacion_settings = 'PUBL_NUEVO_COMENTARIO'
    alt_notification_resp_settings = 'PUBL_RESP_COMENTARIO'
    comentario = models.ForeignKey(Comentario, on_delete=CASCADE)

    def get_settings(self):
        config = super().get_settings()

        if self.comentario.padre:
            config = self.alt_notification_resp_settings

        return config

    @property
    def link(self):
        return self.comentario.publicacion.detalle_url


class NotificacionNuevoSeguidor(Notificacion):
    notificacion_settings = 'NUEVO_SEGUIDOR'
    seguimiento = models.ForeignKey(Seguimiento, on_delete=CASCADE)

    @property
    def link(self):
        return self.seguimiento.usuario.perfil_url


class NotificacionNuevaPublicacion(Notificacion):
    notificacion_settings = 'NUEVA_PUBLICACION'
    publicacion = models.ForeignKey(Publicacion, on_delete=CASCADE)

    @property
    def link(self):
        return self.publicacion.detalle_url
