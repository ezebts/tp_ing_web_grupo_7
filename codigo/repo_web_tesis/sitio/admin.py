from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _

from .models import Comentario, Usuario, Publicacion, Autor


def add_fields_to(fieldsets, fset_name, fields, insert=False):
    idx = 0
    mutables = list(fieldsets)

    for fieldset in mutables:
        name, data = fieldset

        data = data if data else {'fields': tuple()}

        if name == fset_name:
            if insert:
                data['fields'] = (*fields, *data['fields'])
            else:
                data['fields'] += tuple(fields)

            mutables[idx] = (name, data)

        idx += 1

    return tuple(mutables)


class UsuarioAdmin(UserAdmin):
    fieldsets = add_fields_to(
        UserAdmin.fieldsets, _('Permissions'), ['estado'], insert=True)


@admin.register(Publicacion)
class AdminPublicacion(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'fecha_creacion')


@admin.register(Autor)
class AdminAutor(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido')


@admin.register(Comentario)
class AdminComentario(admin.ModelAdmin):
    list_display = ('id', 'texto')


# Admin de usuarios
admin.site.register(Usuario, UsuarioAdmin)
