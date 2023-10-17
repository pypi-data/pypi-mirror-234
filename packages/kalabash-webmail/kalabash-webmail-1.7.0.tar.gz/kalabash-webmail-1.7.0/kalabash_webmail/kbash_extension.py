# coding: utf-8
"""Declare and register the webmail extension."""

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy

from kalabash.core.extensions import KbashExtension, exts_pool
from kalabash.parameters import tools as param_tools

from . import __version__
from . import forms


class Webmail(KbashExtension):
    name = "kalabash_webmail"
    label = "Webmail"
    version = __version__
    description = gettext_lazy("Simple IMAP webmail")
    needs_media = True
    url = "webmail"
    topredirection_url = reverse_lazy("kalabash_webmail:index")

    def load(self):
        param_tools.registry.add("global", forms.ParametersForm, "Webmail")
        param_tools.registry.add("user", forms.UserSettings, "Webmail")


exts_pool.register_extension(Webmail)
