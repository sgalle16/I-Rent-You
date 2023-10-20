from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'cell',
                  'type_of_document', 'number_of_document', 'roll', 'description']
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico',
            'cell': 'Teléfono',
            'type_of_document': 'Tipo de Documento',
            'number_of_document': 'Número de Documento',
            'roll': 'Rol',
            'description': 'Descripción',
        }


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # login(request, user)
            # Redirigir a una página después de iniciar sesión, por ejemplo:
            return ('perfil')

    else:
        form = AuthenticationForm()
    return (request, 'login.html', {'form': form})


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'cell', 'type_of_document',
                  'number_of_document', 'password1', 'password2', 'roll', 'description']
        labels = {
            'username': 'Nombre de Usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico',
            'cell': 'Teléfono',
            'type_of_document': 'Tipo de Documento',
            'number_of_document': 'Número de Documento',
            'password1': 'Contraseña',
            'password2': 'Confirmar Contraseña',
            'roll': 'Rol',
            'description': 'Descripción',
        }

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Este correo electrónico ya está registrado')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].required = True
