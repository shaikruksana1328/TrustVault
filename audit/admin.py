from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):

    list_display = (
        'actor',
        'action',
        'document',
        'target_user',
        'timestamp',
        'ip_address',
    )

    list_filter = ('action', 'timestamp')

    search_fields = (
        'actor__username',
        'document__title',
        'target_user__username',
        'details',
    )

    readonly_fields = (
        'actor',
        'document',
        'target_user',
        'action',
        'details',
        'ip_address',
        'timestamp',
    )