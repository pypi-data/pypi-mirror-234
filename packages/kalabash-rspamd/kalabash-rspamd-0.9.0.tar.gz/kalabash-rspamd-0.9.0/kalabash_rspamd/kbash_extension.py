# -*- coding: utf-8 -*-

"""Rspamd plugin for Kalabash."""

from __future__ import unicode_literals

from django.utils.translation import gettext_lazy

from kalabash.core.extensions import KbashExtension, exts_pool
from kalabash.parameters import tools as param_tools

from . import __version__


class Rspamd(KbashExtension):
    """Rspamd extension class."""

    name = "kalabash_rspamd"
    label = gettext_lazy("Rspamd frontend")
    description = gettext_lazy("Rspamd management frontend")
    version = __version__


exts_pool.register_extension(Rspamd)
