from django.db import models
from django.contrib.auth.models import AbstractUser , User
from django.contrib.auth.models import BaseUserManager

document_types = [
    ('citizenship_id', 'Cedula de Ciudadania'),
    ('identity_id', 'Tarjeta de Identidad.'),
    ('passport_id', 'Pasaporte'),
    ('foreigner_id', 'Cedula de Extranjeria'),
    ('driving_id', 'Licencia de Conducción'),
    ('birth_certificate_id', 'Registro Civil de Nacimiento'),
    ('eps_id', 'Tarjeta de Seguridad Social (EPS)'),
]

role_types = [
    ('lessor', 'Arrendador'),
    ('Tenant', 'Arrendatario'),
]

class User(AbstractUser):   
    username = models.CharField(max_length=200, blank=False, unique=True)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.CharField(max_length=100, blank=False)
    cell = models.CharField(max_length=15, blank=True, null=True)
    type_of_document = models.CharField(max_length=20, choices=document_types)
    number_of_document = models.CharField(max_length=15)
    roll = models.CharField(max_length=20, choices=role_types)
    description = models.TextField()

    def __str__(self):
        return self.username



class CustomUserManager(BaseUserManager):
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Puedes proporcionar un valor predeterminado o vacío para "cell" aquí
        extra_fields.setdefault('cell', '')

        return self._create_user(username, email, password, **extra_fields)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content