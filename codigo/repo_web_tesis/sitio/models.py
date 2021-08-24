from django.db import models
from django.contrib.auth.models import AbstractUser
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
