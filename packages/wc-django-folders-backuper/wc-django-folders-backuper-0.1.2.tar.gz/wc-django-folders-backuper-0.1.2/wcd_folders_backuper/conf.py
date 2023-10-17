from dataclasses import dataclass, field
from pathlib import Path
from django.db import models
from typing import List, Optional, Callable
from px_settings.contrib.django import settings as s


__all__ = 'Settings', 'settings',


def default_path(instance, filename):
    return settings.PATH / filename


@s('WCD_FOLDERS_BACKUPER')
@dataclass
class Settings:
    """
    Example:

    ```python
    WCD_FOLDERS_BACKUPER = {
        "FOLDERS": [],
    }
    ```
    """
    PATH: Path = Path('folder-backups')
    PATH_RESOLVER: Callable[[models.Model, str], Path] = default_path
    FOLDERS: List[str] = field(default_factory=list)


settings = Settings()
