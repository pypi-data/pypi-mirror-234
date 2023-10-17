from __future__ import unicode_literals

from django.apps import AppConfig


class KalabashContactsConfig(AppConfig):
    name = "kalabash_contacts"

    def ready(self):
        from . import handlers
