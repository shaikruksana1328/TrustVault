
from django.db import models
from django.contrib.auth.models import User
from documents.models import Document


class AuditLog(models.Model):

    ACTION_CHOICES = [
        ('UPLOAD', 'Document Uploaded'),
        ('DOWNLOAD', 'Document Downloaded'),
        ('UPDATE', 'Document Updated'),
        ('DELETE', 'Document Deleted'),
        ('GRANT', 'Permission Granted'),
        ('REVOKE', 'Permission Revoked'),
        ('ACCESS_DENIED', 'Access Denied'),
    ]

    actor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='audit_actions'
    )

    document = models.ForeignKey(
        Document,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs'
    )

    target_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='received_audit_actions'
    )

    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES
    )

    details = models.TextField(blank=True)

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.actor} - {self.action} - {self.timestamp}"

