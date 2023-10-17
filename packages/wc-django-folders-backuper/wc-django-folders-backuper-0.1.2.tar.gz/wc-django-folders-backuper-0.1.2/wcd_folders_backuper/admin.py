from django.contrib import admin

from .models import Backup


@admin.register(Backup)
class BackupAdmin(admin.ModelAdmin):
    list_display = 'source', 'backup', 'message', 'created_at',
    readonly_fields = 'source', 'created_at',
    date_hierarchy = 'created_at'
    search_fields = 'backup', 'message', 'created_at',
