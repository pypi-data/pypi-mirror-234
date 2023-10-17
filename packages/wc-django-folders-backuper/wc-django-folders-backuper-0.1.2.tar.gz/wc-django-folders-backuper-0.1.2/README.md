# WebCase files backup

Very simple folders backup script with admin interface to download backup.

## Installation

```sh
pip install wc-django-folders-backuper
```

In `settings.py`:

```python

INSTALLED_APPS += [
  'wcd_folders_backuper',
]
```

## Usage

```python
python manage.py folders_backup
```
