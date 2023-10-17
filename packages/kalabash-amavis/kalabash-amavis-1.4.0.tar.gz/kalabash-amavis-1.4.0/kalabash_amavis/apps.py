# -*- coding: utf-8 -*-

"""AppConfig for amavis."""

from __future__ import unicode_literals

from django.apps import AppConfig


class AmavisConfig(AppConfig):
    """App configuration."""

    name = "kalabash_amavis"
    verbose_name = "Kalabash amavis frontend"

    def ready(self):
        # Import these to force registration of checks and signals
        from . import checks  # NOQA:F401
        from . import handlers  # NOQA:F401
