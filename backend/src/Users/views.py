from django.contrib.auth.views import PasswordChangeView
from .models import Notification
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse_lazy
from django.contrib import messages 
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from Users.forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .forms import ProfileEditForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordChangeForm


def home(request):
    return render(request, 'InformacionEmpresa/home.html')

@login_required
def properties(request):
    return render(request, 'property/property_create.html')

@login_required
def logoutaccount(request):
    logout(request)
    return redirect('home')

def login_view(request):
    if request.method == 'GET':
        return render(request, 'registration/login.html', {'form': AuthenticationForm()})

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:  # Verifica si el usuario está activo
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'El usuario no está activo. Contacta al administrador.')  # Mensaje en caso de usuario inactivo
        else:
            messages.error(request, 'Nombre de usuario y/o contraseña incorrectos.')  # Mensaje en caso de usuario y contraseña incorrectos

    return render(request, 'registration/login.html', {'form': AuthenticationForm()})

def register_view(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data=request.POST)

        if user_creation_form.is_valid():
            user_creation_form.save()

            user = authenticate(username=user_creation_form.cleaned_data['username'], password=user_creation_form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
                return redirect('home')
        else:
            data['form'] = user_creation_form

    return render(request, 'registration/register.html', data)

def view_and_edit_profile(request):
    user = request.user  # Obtén el usuario actualmente autenticado

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('home')  # Puedes redirigir a la página de perfil nuevamente
    else:
        form = ProfileEditForm(instance=user)

    return render(request, 'registration/profile.html', {'form': form})

@login_required
def confirm_delete_account(request):
    if request.method == 'POST':
        # Elimina la cuenta y redirige a la página de inicio u otra página.
        request.user.delete()
        return redirect('home')  # Reemplaza 'home' con la URL adecuada.

    return render(request, 'registration/confirm_delete_account.html')

def notification_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

    # Marcar las notificaciones como leídas
    unread_notifications = notifications.filter(is_read=False)
    unread_notifications.update(is_read=True)

    context = {
        'notifications': notifications,
    }

    return render(request, 'Otros/notify.html', context)

class CustomPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm  # Asegúrate de usar el formulario PasswordChangeForm

    # URL de redirección después de un cambio exitoso (cambiado a 'perfil')
    success_url = reverse_lazy('perfil')

    def form_valid(self, form):
        response = super().form_valid(form)
        update_session_auth_hash(self.request, self.request.user)
        messages.success(self.request, 'Tu contraseña ha sido cambiada con éxito.')
        return response
    