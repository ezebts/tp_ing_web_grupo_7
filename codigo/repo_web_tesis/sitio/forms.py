from django.contrib.auth.forms import UserCreationForm
from .models import Usuario


class RegisterUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = UserCreationForm.Meta.fields + ("email",)

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save(creation=True)

        return user
