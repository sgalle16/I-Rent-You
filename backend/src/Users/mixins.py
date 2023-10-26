from django.contrib.auth.mixins import LoginRequiredMixin
from property.models import Property

# The `LessorUserMixin` class is a mixin that provides functionality for managing lessor users and
# their properties.


class LessorUserMixin(LoginRequiredMixin):
    lessor = None
    properties = []

    def get_lessor(self):
        user = self.request.user
        if user.roll == 'lessor':
            self.lessor = user
            return user
        return None

    def can_create_property(self):
        user = self.request.user
        # Verifica si el usuario es un superusuario(opcional) o lessor
        if user.is_superuser or user.roll == 'lessor':
            return True
        return False

    def get_properties(self):
        lessor = self.get_lessor()
        if lessor:
            # Obtiene las propiedades asociadas al lessor
            properties = Property.objects.filter(owner=lessor)
            self.properties = properties
            return properties
        return None

# The `TenantUserMixin` class is a mixin that provides a method to get the tenant user from the
# request.


class TenantUserMixin(LoginRequiredMixin):
    tenant = None

    def get_tenant(self):
        user = self.request.user
        if user.roll == 'tenant':
            self.tenant = user
            return user
        return None
