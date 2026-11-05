from django.contrib import admin
from .models import Document, DocumentPermission


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'category', 'uploaded_at')
    search_fields = ('title', 'owner__username', 'category')
    list_filter = ('category', 'uploaded_at')


@admin.register(DocumentPermission)
class DocumentPermissionAdmin(admin.ModelAdmin):
    list_display = ('document', 'user', 'permission', 'granted_by', 'created_at')
    search_fields = ('document__title', 'user__username')
    list_filter = ('permission', 'created_at')