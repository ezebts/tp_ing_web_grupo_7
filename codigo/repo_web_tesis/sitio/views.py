import json

from django.contrib.auth import login
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse

from sitio.models import Usuario, Publicacion, CARRERAS
from sitio.errors import EmailNotAllowedError
from sitio.forms import RegisterPublicacionForm, RegisterUserForm, UserChangeImageForm, RegisterComentarioForm
from sitio.services import verify_usuario
from sitio.serializers import ModelJsonSerializer


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
            usuario=request.user if request.user.is_authenticated else None,
            año=año, carreras=filtro_carreras)

        view_filtro = [
            filtro for filtro in filtro_carrera_req.split(',') if filtro
        ]

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
            tit = request.POST.get("titulo")

            publicacion = Publicacion.objects.filter(
                titulo__icontains=tit).first()

            return render(request, 'publicacion.html', {'publicacion': publicacion})
    else:
        form = RegisterPublicacionForm()

    return render(request, 'publicar.html', {"form": form})


@login_required
def editar_publicacion(request, pk):
    publicacion = Publicacion.objects.get(id=pk)
    form = RegisterPublicacionForm(instance=publicacion)

    if request.method == 'POST':

        form = RegisterPublicacionForm(request.POST, instance=publicacion)
        if form.is_valid():
            form.save(request.user)
            return redirect('/')
    context = {'form': form}
    return render(request, 'publicar.html', context)


def publicacion(request):
    publicacion = None
    carreras = dict(carrera for carrera in CARRERAS)

    if request.method == 'GET':
        id = request.GET['id']

        publicacion = Publicacion.objects.get(pk=id)

        if publicacion:
            publicacion.registrar_visita(request.user)

    if not publicacion:
        return redirect(reverse('inicio'))

    return render(request, 'publicacion.html', {'publicacion': publicacion, 'carreras': carreras})


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

    if request.POST and request.POST['action'] == 'seguir':
        request.user.seguir(viewing)

    return render(request, 'cuentas/perfil.html', {'user': viewing, 'public': True})


def comentarios(request, pk):
    if request.method == 'GET' and request.is_ajax():
        comentarios = []
        padre_id = request.GET.get('padre_id') or None
        publicacion = Publicacion.objects.get(pk=pk)

        if publicacion:
            comentarios = publicacion.get_comentarios(padre_id=padre_id)

        response = HttpResponse(ModelJsonSerializer().serialize(
            comentarios, ignored_props=['publicacion']))

        response['Content-Type'] = 'application/json'

        return response

    return redirect(reversed('inicio'))


@login_required
def crear_comentario(request, pk):
    if request.method == 'POST' and request.is_ajax():
        publicacion = Publicacion.objects.get(pk=pk)

        if publicacion:
            body = json.loads(request.body)
            comentario = body.get('texto', None)
            padre_id = body.get('padre_id') or None
            responde_id = body.get('responde_id') or None

            if comentario:
                responde = publicacion.get_comentario(
                    responde_id) if responde_id else None

                padre = publicacion.get_comentario(
                    padre_id) if padre_id else None

                publicacion.comentar(
                    request.user, comentario, padre=padre, responde=responde)

            response = HttpResponse("Ok")
            response['Content-Type'] = 'application/json'

            return response

    return redirect(reversed('inicio'))


@login_required
def get_usuario_notificaciones(request):
    if request.method == 'GET' and request.is_ajax():
        notificaciones = request.user.get_notificaciones()

        response = HttpResponse(ModelJsonSerializer().serialize(
            notificaciones, ignored_props=['usuario']))

        response['Content-Type'] = 'application/json'

        return response

    return redirect(reversed('inicio'))


@login_required
def update_usuario_notificacion(request, pk):
    if request.method == 'POST' and request.is_ajax():
        notificacion = request.user.get_notificacion(pk)

        if notificacion:
            body = json.loads(request.body)

            if body.get('vista'):
                notificacion.marcar_como_vista()

            response = HttpResponse("Ok")
            response['Content-Type'] = 'application/json'

            return response

    return redirect(reversed('inicio'))


@login_required
def create_usuario_seguidor(request, pk):
    if request.method == 'POST' and request.is_ajax():
        usuario = Usuario.objects.get(pk=pk)

        if usuario:
            request.user.seguir(usuario)
            response = HttpResponse("Ok")
            response['Content-Type'] = 'application/json'

            return response

    return redirect(reversed('inicio'))


@login_required
def delete_usuario_seguidor(request, pk):
    if request.method == 'POST' and request.is_ajax():
        usuario = Usuario.objects.get(pk=pk)

        if usuario:
            request.user.dejar_de_seguir(usuario)
            response = HttpResponse("Ok")
            response['Content-Type'] = 'application/json'

            return response

    return redirect(reversed('inicio'))


def usuario_publicaciones(request, pk):
    if request.method == 'GET':
        publicaciones = Publicacion.objects.filter(usuario__id=pk)

        response = HttpResponse(ModelJsonSerializer().serialize(
            publicaciones, ignored_props=['usuario']))

        response['Content-Type'] = 'application/json'

        return response

    return redirect(reversed('inicio'))


def usuario_seguidores(request, pk):
    if request.method == 'GET':
        usuario = Usuario.objects.get(pk=pk)

        if usuario:
            response = HttpResponse(ModelJsonSerializer().serialize(
                usuario.get_seguidores(), fields=['username', 'perfil_url', 'imagen_url']))
        else:
            response = HttpResponse('Not Found', status=404)

        response['Content-Type'] = 'application/json'

        return response

    return redirect(reversed('inicio'))


def usuario_seguidos(request, pk):
    if request.method == 'GET':
        usuario = Usuario.objects.get(pk=pk)

        if usuario:
            response = HttpResponse(ModelJsonSerializer().serialize(
                usuario.get_siguiendo(), fields=['username', 'perfil_url', 'imagen_url']))
        else:
            response = HttpResponse('Not Found', status=404)

        response['Content-Type'] = 'application/json'

        return response

    return redirect(reversed('inicio'))
