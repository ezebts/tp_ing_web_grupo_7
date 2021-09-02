from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Usuario, Publicacion


class RegisterUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = UserCreationForm.Meta.fields + ("email",)

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save(creation=True)

        return user


class RegisterPublicacionForm(ModelForm):
    class Meta:
        model = Publicacion
        fields = ['titulo', 'resumen', 'fecha_creacion', 'imagen', 'archivo']
