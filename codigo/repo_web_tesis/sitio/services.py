from django.conf import settings
from django.dispatch import receiver
from django.shortcuts import reverse

from sitio.models import Usuario, ESTADOS_USUARIO
from sitio.errors import EmailNotAllowedError, UserBannedError
from sitio.security import token_factory

user_activation_tokens = token_factory(lambda user, **kwargs: user.estado)


def auth_usuario(usuario):
    if usuario.estado == ESTADOS_USUARIO.BLOQUEADO_PERM:
        raise UserBannedError("Your account has been banned permanently")
    elif usuario.estado == ESTADOS_USUARIO.BLOQUEADO_TEMP:
        raise UserBannedError("Your account has been banned temporally")

    return usuario


def create_edit_usuario(usuario):
    valid_emails = settings.ALLOWED_EMAIL_DOMAINS

    valid_format = filter(
        lambda email: email.format.search(usuario.email),
        valid_emails
    )

    if not any(valid_format):
        raise EmailNotAllowedError(usuario.email, valid_emails)

    # No importa si se crea o edita
    # solo indicar creation=True cuándo
    # se quiera validar si se está creando uno nuevo
    usuario.save(creation=True)

    return usuario


def create_edit_publicacion(usuario, publicacion):
    publicacion.usuario = usuario
    publicacion.save()

    return publicacion


@receiver(Usuario.on_created.new)
def confirm_usuario(usuario, **kwargs):
    """
    Envia un email de confirmación al usuario
    """
    uid, token = user_activation_tokens.make_token(usuario)
    email_settings = dict(settings.EMAILS.get('CONFIRM_USER_EMAIL'))

    link = settings.HOST + reverse(
        email_settings.pop('ACTIVATION_URL'),
        kwargs={
            'uid': uid,
            'token': token
        })[1:]

    usuario.send_email(**email_settings, context={'link': link})


def verify_usuario(usuario, sign, token):
    verified = False
    usuario_id = user_activation_tokens.decode_sign(sign)

    if usuario:
        if str(usuario.pk) == usuario_id:
            if usuario.estado == ESTADOS_USUARIO.NO_VERIFICADO:
                if user_activation_tokens.check_token(usuario, token):
                    verified = True
                    usuario.estado = ESTADOS_USUARIO.VERIFICADO
                    usuario.save()

    if not verified:
        usuario = None

    return usuario

