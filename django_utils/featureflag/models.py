from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from model_utils.models import TimeStampedModel


class ClientFlagManager(models.Manager):
    """ Flag model manager """

    def is_active(self, slug: str,  host_name: str) -> bool:
        """
        :param slug: client flag slug
        :param host_name: client host_name
        :return: flag status for current request
        """
        try:
            feature = self.get(slug=slug)
        except ObjectDoesNotExist:
            return False

        if feature.everyone is False:
            return False
        elif feature.everyone is True:
            return True

        active_host_names = [client.host_name for client in feature.client.all()]
        return True if host_name in active_host_names else False


class ClientFlag(TimeStampedModel):
    """
    A feature flag model. Feature that depend on current request.
    You can define who the flag is active to.
    """
    slug = models.SlugField(max_length=100, unique=True)  #:
    #: Flag override any further settings if not ``Unknown`` status. Options
    #: are: ``Yes``, ``No``, ``Unknown``
    everyone = models.BooleanField(null=True, blank=True, help_text=(
        'Flip this flag on (Yes) or off (No) for everyone, overriding all '
        'other settings. Leave as Unknown to use normally.'))
    #: Enable for a client (must provide host_name field)
    client = models.ManyToManyField(settings.FEATUREFLAG_CLIENT_MODEL, blank=True, help_text=(
        'Activate this flag for these sites.'))
    #: Enable flag for site groups
    note = models.TextField(blank=True, help_text=(
        'Note where this Flag is used.'))  #:

    class Meta:
        verbose_name_plural = "Client Flags"

    def __unicode__(self):
        return self.slug

    objects = ClientFlagManager()


class SwitchManager(models.Manager):
    """
    Switch model manager
    """

    def is_active(self, slug: str) -> bool:
        """
        :param slug: switch slug
        :return: switch status
        """
        try:
            status = self.get(slug=slug).active
        except ObjectDoesNotExist:
            return False
        return status


class Switch(TimeStampedModel):
    """
    Switch model. Feature that does not depend on current request.
    Just global on/off switch.
    """
    slug = models.SlugField(max_length=100, unique=True)  #:
    #: On/off flag
    active = models.BooleanField(default=False, help_text=(
        'Is this flag active?'))
    note = models.TextField(blank=True, help_text=(
        'Note where this Switch is used.'))  #:

    class Meta:
        verbose_name_plural = "Switches"

    def __unicode__(self):
        return self.slug

    objects = SwitchManager()
