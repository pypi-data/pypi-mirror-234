"""AppConfig for stats."""

from django.apps import AppConfig


class SieveFiltersConfig(AppConfig):
    """App configuration."""

    name = "kalabash_sievefilters"
    verbose_name = "Sieve filters editor for Kalabash"

    def ready(self):
        from . import handlers
