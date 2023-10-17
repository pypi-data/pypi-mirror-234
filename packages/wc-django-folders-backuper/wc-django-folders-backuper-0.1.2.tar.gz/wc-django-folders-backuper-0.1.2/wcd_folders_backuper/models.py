from datetime import datetime
from typing import List, Optional, Sequence, Union
from uuid import uuid4, UUID
from django.db import models
from django.utils.translation import pgettext_lazy

from .conf import settings


__all__ = 'Token', 'TokenUserConnection',



class BackupQuerySet(models.QuerySet):
    pass


class Backup(models.Model):
    # type: models.Manager[TokenQuerySet]
    objects = BackupQuerySet.as_manager()

    class Meta:
        verbose_name = pgettext_lazy('wcd_fb', 'Backup')
        verbose_name_plural = pgettext_lazy('wcd_fb', 'Backups')
        ordering = '-created_at', '-id',

    backup = models.FileField(
        pgettext_lazy('wcd_fb', 'Backup'),
        upload_to=settings.PATH_RESOLVER, null=False, blank=False,
    )
    source = models.TextField(
        pgettext_lazy('wcd_fb', 'Source location'), null=False, blank=False,
    )

    message = models.TextField(
        pgettext_lazy('wcd_fb', 'Message'), null=False, blank=True,
    )
    created_at = models.DateTimeField(
        pgettext_lazy('wcd_fb', 'Created at'), auto_now_add=True,
    )

    def __str__(self):
        return f'{self.backup.url}'
