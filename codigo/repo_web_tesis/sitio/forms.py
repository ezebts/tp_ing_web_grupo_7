from django.core.exceptions import ValidationError
from django.forms import ModelForm, EmailInput
from django.contrib.auth.forms import UserCreationForm

from sitio.models import Usuario, Publicacion
from sitio.errors import EmailNotAllowedError
from sitio.services import create_edit_publicacion, create_edit_usuario


class RegisterUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'example@any.ucse.edu.ar'
        self.fields['email'].label = 'example@any.ucse.edu.ar'

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = UserCreationForm.Meta.fields + ("email",)

    def save(self, commit=True):
        usuario_data = super().save(commit=False)

        if commit:
            try:
                usuario_data = create_edit_usuario(usuario_data)
            except ValidationError as error:
                usuario_data = None
                self.add_error(error.code, error.message)

        return usuario_data


class RegisterPublicacionForm(ModelForm):
    class Meta:
        model = Publicacion
        fields = ['titulo', 'resumen', 'fecha_creacion', 'imagen', 'archivo']

    def save(self, usuario, commit=True):
        pub_data = super().save(commit=False)

        if commit:
            pub_data = create_edit_publicacion(usuario, pub_data)

        return pub_data


class UserChangeImageForm(ModelForm):
    class Meta:
        model = Usuario
        fields = ('imagen',)
