from django.contrib.auth import login
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings

from sitio.models import Comentario, Publicacion, Autor, CARRERAS, Publicaciones
from sitio.errors import EmailNotAllowedError
from sitio.forms import RegisterPublicacionForm, RegisterUserForm, UserChangeImageForm, RegisterComentarioForm
from sitio.services import verify_usuario


def inicio(request):
    publicaciones = Publicacion.objects.all()
    #publicaciones = Publicaciones.all()
    return render(request, 'inicio.html', {'publicaciones': publicaciones})

def registro(request):
    form = RegisterUserForm()

    if request.method == "POST":
        form = RegisterUserForm(request.POST)

        if form.is_valid():
            user = form.save()

            if user:
                login(request, user)
                return redirect(reverse(settings.REGISTER_REDIRECT_URL))

    return render(
        request,
        "cuentas/registro.html",
        {"form": form}
    )

@login_required
def publicar(request):  # Problema para cargar los archivos
    if request.method == 'POST':
        form = RegisterPublicacionForm(request.POST, request.FILES)

        if form.is_valid():
            form.save(request.user)

            return redirect(reverse('inicio'))
    else:
        form = RegisterPublicacionForm()

    return render(request, 'publicar.html', {"form": form})

def publicacion(request):
    if request.method == 'GET':
        id = request.GET['id']
        publicacion = Publicacion.objects.get(pk=id)

        comentarios = Comentario.objects.filter(publicacion=id)

        autores = Autor.objects.filter(publicacion=id)

    return render(request, 'publicacion.html', {'publicacion': publicacion,
                                                'comentarios': comentarios,
                                                'autores': autores, })

def filtrar(request):
    if request.method == 'GET':
        año = request.GET['año']
        carrera = request.GET['carrera']

        publicaciones = Publicaciones.filtrar(año,carrera)

        #publicaciones = (Publicacion.objects
            #.filter(año_creacion__year=f_año)
            #.filter(carrera=f_carrera)
            #.order_by('año_creacion'))

    return render(request, 'inicio.html', {'publicaciones':publicaciones})

@login_required
def confirmar_email(request, uid, token):
    validated = verify_usuario(request.user, uid, token)

    if validated:
        return redirect('perfil')
    else:
        return redirect('inicio')

@login_required
def actualizar_perfil_img(request):
    data = request.GET
    if request.method == 'POST':
        data = request.POST
        form = UserChangeImageForm(request.POST, request.FILES)

        if form.is_valid():
            frmdata = form.save(commit=False)
            request.user.imagen = frmdata.imagen
            request.user.save()

    return redirect(data.get('next', 'inicio'))

@login_required
def perfil(request):
    return render(request, 'cuentas/perfil.html')

@login_required
def comentar(request):
    if request.method == 'POST':
        id = request.GET['id_publicacion']
        publicacion= Publicaciones.get(pk=id)
        form = RegisterComentarioForm(request.POST)

        if form.is_valid():
            form.save(id)
            
    return redirect('publicacion')