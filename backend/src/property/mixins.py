from django.http import Http404
from Users.mixins import LessorUserMixin

# The `PropertyLessorMixin` class is a mixin that checks if the current user is the owner of an object
# before allowing access to it.
class PropertyLessorMixin(LessorUserMixin, object):
    def get_object(self, *args, **kwargs):
        lessor = self.get_lessor()
        obj = super(PropertyLessorMixin, self).get_object(*args, **kwargs)
        if obj.owner == lessor:
            return obj
        else:
            raise Http404
