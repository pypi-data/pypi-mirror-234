from django.apps import AppConfig
from django.utils.translation import pgettext_lazy

from .discovery import autodiscover


__all__ = ('FoldersBackuperConfig',)


class FoldersBackuperConfig(AppConfig):
    name = 'wcd_folders_backuper'
    verbose_name = pgettext_lazy('wcd_fb', 'Folders backuper')
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        from . import handlers
        autodiscover()
