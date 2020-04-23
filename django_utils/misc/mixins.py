from django.core import urlresolvers
from django.contrib.contenttypes.models import ContentType


class AdminLinkMixin(object):
    """ Mixin that gives generic admin url to change form """

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse(
            f"admin:{content_type.app_label}_{content_type.model}_change", args=(self.id,))
