"""repo_web_tesis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from typing import Pattern
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from sitio import views

urlpatterns = [
    # Admin urls
    path('admin/', admin.site.urls),

    # Auth management urls
    path('auth/', include('django.contrib.auth.urls')),

    # Sitio urls
    path('', views.inicio, name='inicio'),
    path('search/', include('haystack.urls')),
    path('perfil', views.perfil, name='perfil'),
    path('perfil/<str:pk>', views.perfil_publico, name='perfil_publico'),
    path('perfil/actualizar-foto/',
         views.actualizar_perfil_img, name='actualizar_foto'),
    path("registro/", views.registro, name="registro"),
    path('repositorio/publicar', views.publicar, name='publicar'),
    path('editar_publicacion/<str:pk>/',
         views.editar_publicacion, name='editar_publicacion'),
    path('repositorio/publicacion', views.publicacion, name='publicacion'),
    path('registro/confirmar-email/<uid>/<token>',
         views.confirmar_email, name='confirmar_email'),

    # Api endpoints
    path('api/publicaciones/<str:pk>/comentarios',
         views.comentarios, name='api_publicaciones_comentarios'),

    path('api/publicaciones/<str:pk>/nuevo-comentarios',
         views.crear_comentario, name='api_publicaciones_nuevo_comentarios'),

    path('api/usuarios/notificaciones',
         views.get_usuario_notificaciones, name='api_get_notificaciones_usuario'),

    path('api/usuarios/notificaciones/<str:pk>',
         views.update_usuario_notificacion, name='api_update_notificacion_usuario'),

    path('api/usuarios/<str:pk>/seguidores',
         views.create_usuario_seguidor, name='api_seguir_usuario'),

    path('api/usuarios/<str:pk>/publicaciones',
         views.usuario_publicaciones, name='api_usuarios_publicaciones'),

    path('robots.txt', views.robots_txt)

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
