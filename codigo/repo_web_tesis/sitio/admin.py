from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

# Admin de usuarios
admin.site.register(Usuario, UserAdmin)