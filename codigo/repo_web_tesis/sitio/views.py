from django.contrib.auth import login
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings

from sitio.models import Usuario, Publicacion, CARRERAS
from sitio.errors import EmailNotAllowedError
from sitio.forms import RegisterPublicacionForm, RegisterUserForm, UserChangeImageForm, RegisterComentarioForm
from sitio.services import verify_usuario


def inicio(request):
    context = {}
    if request.method == 'GET':
        año = request.GET.get('filtro_anio', None)

        if año:
            try:
                año = int(año)
            except:
                año = None

        action = request.GET.get('action', None)

        filtro_carrera_req = request.GET.get('filtro_carreras', '')

        carreras_mapping = dict([(carrera[1], carrera[0])
                                for carrera in CARRERAS])

        filtro_carreras = [carreras_mapping[str(filtro).strip(
        )] for filtro in filtro_carrera_req.split(',') if filtro]

        publicaciones = Publicacion.objects.filtrar(
            año=año, carreras=filtro_carreras)

        view_filtro = [
            filtro for filtro in filtro_carrera_req.split(',') if filtro]

        context = {'publicaciones': publicaciones, 'carreras': CARRERAS,
                   'filtro_carreras': view_filtro, 'filtro_anio': año, 'action': action}

    return render(request, 'inicio.html', context)


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
def publicar(request):
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

        # Logica para comentar usando el ModelForm

    return render(request, 'publicacion.html', {'publicacion': publicacion})


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


def perfil_publico(request, pk):
    if not pk or pk == request.user.pk:
        redirect(reverse('perfil'))

    viewing = Usuario.objects.get(pk=pk)

    return render(request, 'cuentas/perfil.html', {'user': viewing, 'public': True})



