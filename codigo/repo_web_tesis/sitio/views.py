from .models import Publicacion
from django.contrib.auth import login
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required

from .forms import RegisterPublicacionForm, RegisterUserForm


# Create your views here.
def inicio(request):
    return render(request, 'inicio.html', {})

def repositorio(request):
    publicaciones = Publicacion.objects.all()
    return render(request, 'repositorio.html', {'publicaciones':publicaciones})

def registro(request):
    form = RegisterUserForm()

    if request.method == "POST":
        form = RegisterUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect(reverse("perfil"))

    return render(
        request,
        "cuentas/registro.html",
        {"form": form}
    )


def publicar(request): # Problema para cargar los archivos
    if request.method == 'POST':
        form = RegisterPublicacionForm(request.POST, request.FILES)

        if form.is_valid():
            publi = form.save()
    else:
        form = RegisterPublicacionForm()
    
    return render(request, 'publicar.html', {"form": form})


@login_required
def pefil(request):
    return render(request, 'cuentas/perfil.html')
