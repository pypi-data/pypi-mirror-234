from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Backup


@receiver(post_delete, sender=Backup)
def clear_file_on_delete(sender, instance: Backup, **kwargs):
    if instance.backup:
        instance.backup.delete(save=False)
