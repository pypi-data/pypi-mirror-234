"""AppConfig for webmail."""

from django.apps import AppConfig


class WebmailConfig(AppConfig):
    """App configuration."""

    name = "kalabash_webmail"
    verbose_name = "Simple webmail for Kalabash"

    def ready(self):
        from . import handlers
