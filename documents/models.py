from django.db import models
from django.contrib.auth.models import User


class Document(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='private_documents/')
    category = models.CharField(max_length=100, default='General')
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_documents'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title

class DocumentPermission(models.Model):

    PERMISSION_CHOICES = [
        ('READ', 'Read'),
        ('EDIT', 'Edit'),
    ]

    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='permissions'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='document_permissions'
    )

    permission = models.CharField(
        max_length=10,
        choices=PERMISSION_CHOICES
    )

    granted_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='granted_permissions'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['document', 'user'],
                name='unique_document_user_permission'
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.document.title} - {self.permission}"