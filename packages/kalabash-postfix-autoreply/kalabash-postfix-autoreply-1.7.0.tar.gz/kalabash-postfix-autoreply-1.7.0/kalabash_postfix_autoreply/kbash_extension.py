# -*- coding: utf-8 -*-

"""
Postfix auto-replies plugin.

This module provides a way to integrate Kalabash auto-reply
functionality into Postfix.

"""

from django.utils.translation import gettext_lazy

from kalabash.admin import models as admin_models
from kalabash.core.extensions import KbashExtension, exts_pool
from kalabash.parameters import tools as param_tools
from kalabash.transport import models as tr_models

from . import __version__, forms


class PostfixAutoreply(KbashExtension):
    """Auto-reply (vacation) functionality using Postfix."""

    name = "kalabash_postfix_autoreply"
    label = "Postfix autoreply"
    version = __version__
    description = gettext_lazy(
        "Auto-reply (vacation) functionality using Postfix")

    def load(self):
        param_tools.registry.add(
            "global", forms.ParametersForm, gettext_lazy("Automatic replies"))

    def load_initial_data(self):
        """Create records for existing domains."""
        for dom in admin_models.Domain.objects.all():
            trans, created = tr_models.Transport.objects.get_or_create(
                pattern="autoreply.{}".format(dom.name),
                service="autoreply")


exts_pool.register_extension(PostfixAutoreply)
