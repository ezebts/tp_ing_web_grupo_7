from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


def token_factory(get_hash_value):
    class Factory(PasswordResetTokenGenerator):
        def _make_hash_value(self, user, timestamp):
            return (
                str(user.pk) + str(timestamp) +
                str(get_hash_value(user=user, timestamp=timestamp))
            )

        def make_token(self, user, encoding='utf-8'):
            """
            Devuelve un resultado (encoded_sign, token)
            """
            token = super().make_token(user)
            sign = urlsafe_base64_encode(
                bytes(str(user.pk), encoding=encoding))

            return sign, token

        def check_token(self, user, token):
            """
            Verifica que el token sea correcto
            """
            try:

                if not user or not token:
                    return False

                return super().check_token(user, token)

            except (TypeError, ValueError, OverflowError):
                return False

        def decode_sign(self, sign, encoding='utf-8'):
            return urlsafe_base64_decode(sign).decode(encoding)

    return Factory()
