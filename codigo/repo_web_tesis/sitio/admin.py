from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Comentario, Usuario, Publicacion, Autor

# Admin de usuarios
admin.site.register(Usuario, UserAdmin)


@admin.register(Publicacion)
class AdminPublicacion(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'fecha_creacion')


@admin.register(Autor)
class AdminAutor(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido')


@admin.register(Comentario)
class AdminComentario(admin.ModelAdmin):
    list_display = ('id', 'texto')