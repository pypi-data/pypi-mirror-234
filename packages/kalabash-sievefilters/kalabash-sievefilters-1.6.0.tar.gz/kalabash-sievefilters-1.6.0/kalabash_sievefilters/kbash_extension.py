# coding: utf-8
"""Declare and register the sievefilters extension."""

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy

from kalabash.core.extensions import KbashExtension, exts_pool
from kalabash.parameters import tools as param_tools

from . import __version__
from . import forms


class SieveFilters(KbashExtension):
    name = "kalabash_sievefilters"
    label = gettext_lazy("Sieve filters")
    version = __version__
    description = gettext_lazy("Plugin to easily create server-side filters")
    url = "sfilters"
    topredirection_url = reverse_lazy("kalabash_sievefilters:index")

    def load(self):
        param_tools.registry.add(
            "global", forms.ParametersForm, gettext_lazy("Sieve filters"))
        param_tools.registry.add(
            "user", forms.UserSettings, gettext_lazy("Message filters"))


exts_pool.register_extension(SieveFilters)
