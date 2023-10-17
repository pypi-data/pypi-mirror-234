# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import gettext_lazy


def load_rspamd_settings():
    """Load rspamd settings.

    This function must be manually called (see :file:`urls.py`) in
    order to load base settings.
    """
    from kalabash.parameters import tools as param_tools
    from . import app_settings
    from .api.v2 import serializers

    param_tools.registry.add(
        "global", app_settings.ParametersForm, gettext_lazy("Rspamd"))
    param_tools.registry.add2(
        "global", "kalabash_rspamd", gettext_lazy("Rspamd"),
        app_settings.RSPAMD_PARAMETERS_STRUCT,
        serializers.RspamdSettingsSerializer)


class KalabashRspamdConfig(AppConfig):
    name = 'kalabash_rspamd'
    verbose_name = "Kalabash connector for Rspamd."

    def ready(self):
        from . import handlers  # NOQA:F401

        load_rspamd_settings()
