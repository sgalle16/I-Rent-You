from Users.mixins import LessorUserMixin
from django.core.exceptions import PermissionDenied


# The PropertyLessorMixin class checks if the current user is the owner of an object and raises an
# exception if not.
class PropertyLessorMixin(LessorUserMixin):
    def check_ownership(self, obj):
        lessor = self.get_lessor()
        if obj.owner == lessor:
            return obj
        else:
            raise PermissionDenied(
                "You don't have permission to access this object")

    def get_object(self, *args, **kwargs):
        obj = super(PropertyLessorMixin, self).get_object(*args, **kwargs)
        return self.check_ownership(obj)
