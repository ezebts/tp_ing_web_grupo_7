from io import StringIO
from django.core.exceptions import ValidationError


class EmailNotAllowedError(ValidationError):
    def __init__(self, email, formats, *args, **kwargs):
        error = None
        msg = StringIO()
        msg.write(
            f"Email '{email}' not allowed, must be from domain or subdomains of: ")

        valid_domains = [email.domain for email in formats]

        for domain in valid_domains:
            msg.write(f"'@{ domain }', ")

        error = msg.getvalue()

        msg.close()

        super().__init__(error[:len(error)-2], 'email', *args, **kwargs)


class UserBannedError(ValidationError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
