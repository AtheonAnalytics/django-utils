from django.db import models
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple

from .models import ClientFlag, Switch


@admin.register(ClientFlag)
class ClientFlagAdmin(admin.ModelAdmin):
    list_editable = ('everyone',)
    list_display = ('slug', 'note', 'everyone', )
    formfield_overrides = {
        models.ManyToManyField: {'widget': FilteredSelectMultiple(
            verbose_name='Options', is_stacked=False, )},
    }


@admin.register(Switch)
class SwitchAdmin(admin.ModelAdmin):
    list_display = ('slug', 'note', 'active')
    list_editable = ('active',)
    formfield_overrides = {
        models.ManyToManyField: {'widget': FilteredSelectMultiple(
            verbose_name='Options', is_stacked=False, )},
        }

