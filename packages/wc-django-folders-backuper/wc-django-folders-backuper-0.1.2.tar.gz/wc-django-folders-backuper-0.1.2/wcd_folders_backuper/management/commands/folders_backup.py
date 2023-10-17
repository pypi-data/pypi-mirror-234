from typing import List, Optional
from django.core.management.base import BaseCommand
from wcd_folders_backuper.services import backuper
from wcd_folders_backuper.conf import settings
from logging import getLogger


logger = getLogger(__name__)


class Command(BaseCommand):
    help = 'Backups folders.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--folder', '-f', nargs='+', type=str,
            help='Folders to collect from. If none passed - default will be ',
        )
        parser.add_argument(
            '--message', '-m', nargs='?', type=str, default=None,
            help='Add a message to describe current backup.',
        )

    def handle(
        self,
        *args,
        folder: List[str] = [],
        message: Optional[str] = None,
        **options
    ):
        folders: List[str] = (
            folder
            if folder is not None and len(folder) > 0 else
            settings.FOLDERS
        )

        logger.debug('Folders list: %s' % folders)

        if len(folders) < 1:
            self.stdout.write(self.style.ERROR('No folders specified.'))
            return

        backuper.backup_folders(
            folders,
            message=message or '',
            report_error=lambda *args: self.stdout.write(self.style.WARNING(*args))
        )
