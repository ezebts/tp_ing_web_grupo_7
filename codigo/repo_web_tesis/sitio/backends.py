from django.contrib.auth.backends import ModelBackend
from sitio.services import auth_usuario


class UsuarioAuthBackend(ModelBackend):
    def user_can_authenticate(self, user):
        valid = super().user_can_authenticate(user)

        if valid:
            auth_usuario(user)

        return valid
