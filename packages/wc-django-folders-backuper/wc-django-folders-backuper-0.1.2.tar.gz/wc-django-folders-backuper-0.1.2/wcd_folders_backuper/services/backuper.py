from typing import List
import tarfile
import os
from uuid import uuid4
from django.utils import timezone
from logging import getLogger
from django.core.files import File

from wcd_folders_backuper.models import Backup


__all__ = 'backup_folders',

logger = getLogger(__name__)


def backup_folders(
    folders: List[str],
    message: str = '',
    report_error=lambda *args: logger.warning(*args),
):
    for folder in folders:
        folder = folder.rstrip('/')
        name = os.path.basename(folder)
        now = timezone.now()
        str_now = (
            now.isoformat()
            .replace(':', '-')
            .replace('.', '-')
            .replace('+', 'plus')
        )
        filename = f'{uuid4().hex}-{name}-{str_now}.tgz'
        tmp_file = f'/tmp/{filename}'

        with tarfile.open(tmp_file, 'w:gz') as tar:
            tar.add(folder, name)

        backup = Backup(
            backup='', source=folder, message=message, created_at=now,
        )
        with open(tmp_file, 'rb') as f:
            backup.backup.save(filename, File(f))

        os.remove(tmp_file)
