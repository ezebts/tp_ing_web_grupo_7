from django.urls import path

from . import views

urlpatterns = [
    # Inicio
    path('', views.inicio)
]
