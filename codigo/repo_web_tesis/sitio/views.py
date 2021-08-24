from django.contrib.auth import login
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required

from .forms import RegisterUserForm


# Create your views here.


def inicio(request):
    return render(request, 'inicio.html', {})


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


@login_required
def pefil(request):
    return render(request, 'cuentas/perfil.html')
