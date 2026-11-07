
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import FileResponse, HttpResponseForbidden
from pathlib import Path

from .models import Document, DocumentPermission
from .forms import DocumentForm, DocumentPermissionForm
from audit.models import AuditLog
from django.views.decorators.http import require_POST

@login_required
def document_list_view(request):

    documents = Document.objects.filter(
        Q(owner=request.user) |
        Q(permissions__user=request.user)
    ).distinct()

    search_query = request.GET.get('search', '')
    upload_date = request.GET.get('upload_date', '')

    if search_query:
        documents = documents.filter(
            Q(title__icontains=search_query) |
            Q(owner__username__icontains=search_query) |
            Q(category__icontains=search_query)
        )

    if upload_date:
        documents = documents.filter(
            uploaded_at__date=upload_date
        )

    documents = documents.order_by('-uploaded_at')

    return render(
        request,
        'documents/document_list.html',
        {
            'documents': documents,
            'search_query': search_query,
            'upload_date': upload_date
        }
    )


# Show documents shared with the logged-in user
@login_required
def shared_documents_view(request):

    shared_documents = Document.objects.filter(
        permissions__user=request.user
    ).exclude(
        owner=request.user
    ).select_related(
        'owner'
    ).distinct().order_by('-uploaded_at')

    return render(
        request,
        'documents/shared_documents.html',
        {
            'documents': shared_documents
        }
    )


# Manage permissions granted by the logged-in document owner
@login_required
def access_management_view(request):

    # Only document owners can manage their permissions
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.role != 'OWNER':
        return HttpResponseForbidden(
            'Only document owners can access permission management.'
        )

    permissions = DocumentPermission.objects.filter(
        document__owner=request.user
    ).select_related(
        'document',
        'user'
    ).order_by('-created_at')

    return render(
        request,
        'documents/access_management.html',
        {
            'permissions': permissions
        }
    )



# Upload a new document
@login_required
def upload_document_view(request):

    if not hasattr(request.user, 'userprofile') or request.user.userprofile.role != 'OWNER':
        messages.error(request, 'Only Document Owners can upload documents.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            document = form.save(commit=False)
            document.owner = request.user
            document.save()

            AuditLog.objects.create(
                actor=request.user,
                document=document,
                action='UPLOAD',
                details='Document uploaded successfully.'
                ip_address=request.META.get('REMOTE_ADDR')
            )

            messages.success(request, 'Document uploaded successfully!')
            return redirect('document_list')

    else:
        form = DocumentForm()

    return render(
        request,
        'documents/upload.html',
        {'form': form}
    )


# Secure document download
@login_required
def download_document_view(request, document_id):

    document = get_object_or_404(Document, id=document_id)

    # Check document ownership
    is_owner = document.owner == request.user

    # Check READ or EDIT permission
    has_permission = DocumentPermission.objects.filter(
        document=document,
        user=request.user,
        permission__in=['READ', 'EDIT']
    ).exists()

    # Block unauthorized users
    if not is_owner and not has_permission:

        AuditLog.objects.create(
            actor=request.user,
            document=document,
            action='ACCESS_DENIED',
            details='Unauthorized document download attempt.',
            ip_address=request.META.get('REMOTE_ADDR')
        )

        return HttpResponseForbidden(
            'Access denied. You do not have permission to download this document.'
        )

    # Record successful download
    AuditLog.objects.create(
        actor=request.user,
        document=document,
        action='DOWNLOAD',
        details='Document downloaded successfully.',
        ip_address=request.META.get('REMOTE_ADDR')
    )

    return FileResponse(
        document.file.open('rb'),
        as_attachment=True,
        filename=Path(document.file.name).name
    )

# Share a document with another user
@login_required
def share_document_view(request, document_id):

    document = get_object_or_404(Document, id=document_id)

    if document.owner != request.user:
        AuditLog.objects.create(
            actor=request.user,
            document=document,
            action='ACCESS_DENIED',
            details='Unauthorized document sharing attempt.',
            ip_address=request.META.get('REMOTE_ADDR')
        )
        return HttpResponseForbidden(
            'Access denied. Only the document owner can share this document.'
        )

    if request.method == 'POST':
        form = DocumentPermissionForm(
            request.POST,
            current_user=request.user
        )

        if form.is_valid():
            shared_user = form.cleaned_data['user']
            permission_type = form.cleaned_data['permission']

            permission, created = DocumentPermission.objects.update_or_create(
                document=document,
                user=shared_user,
                defaults={
                    'permission': permission_type,
                    'granted_by': request.user
                }
            )

            AuditLog.objects.create(
                actor=request.user,
                document=document,
                target_user=shared_user,
                action='GRANT',
                details=f'{permission_type} permission granted or updated.',
                ip_address=request.META.get('REMOTE_ADDR')
            )

            messages.success(
                request,
                'Permission granted successfully!' if created
                else 'Permission updated successfully!'
            )

            return redirect('document_list')

    else:
        form = DocumentPermissionForm(current_user=request.user)

    return render(
        request,
        'documents/share.html',
        {'form': form, 'document': document}
    )

# Revoke document access
@login_required
@require_POST
def revoke_permission_view(request, document_id, permission_id):
    document = get_object_or_404(Document, id=document_id)

    # Block anyone who is not the document owner
    if document.owner != request.user:
        AuditLog.objects.create(
            actor=request.user,
            document=document,
            action='ACCESS_DENIED',
            details='Attempted to revoke document permission without ownership.',
            ip_address=request.META.get('REMOTE_ADDR')
        )
        return HttpResponseForbidden(
            'You are not allowed to revoke this permission.'
        )

    permission = get_object_or_404(
        DocumentPermission,
        id=permission_id,
        document=document
    )

    # Record the successful revocation
    AuditLog.objects.create(
        actor=request.user,
        document=document,
        target_user=permission.user,
        action='REVOKE',
        details=f'Permission revoked for {permission.user.username}.',
        ip_address=request.META.get('REMOTE_ADDR')
    )

    permission.delete()

    messages.success(request, 'Document access revoked successfully.')

    return redirect('access_management')

# Edit document details
@login_required
def edit_document_view(request, document_id):

    document = get_object_or_404(Document, id=document_id)

    # Check whether the user owns the document
    is_owner = document.owner == request.user

    # Check whether the user has EDIT permission
    has_edit_permission = DocumentPermission.objects.filter(
        document=document,
        user=request.user,
        permission='EDIT'
    ).exists()

    # Block users without edit permission
    if not is_owner and not has_edit_permission:

        AuditLog.objects.create(
            actor=request.user,
            document=document,
            action='ACCESS_DENIED',
            details='Unauthorized document edit attempt.',
            ip_address=request.META.get('REMOTE_ADDR')
        )

        return HttpResponseForbidden(
            'Access denied. You do not have permission to edit this document.'
        )

    if request.method == 'POST':

        form = DocumentForm(
            request.POST,
            request.FILES,
            instance=document
        )

        if form.is_valid():

            form.save()

            AuditLog.objects.create(
                actor=request.user,
                document=document,
                action='UPDATE',
                details='Document updated successfully.',
                ip_address=request.META.get('REMOTE_ADDR')
            )

            messages.success(request, 'Document updated successfully!')
            return redirect('document_list')

    else:
        form = DocumentForm(instance=document)

    return render(
        request,
        'documents/edit.html',
        {'form': form, 'document': document}
    )

# Delete a document securely

@login_required
@require_POST
def delete_document_view(request, document_id):

    document = get_object_or_404(Document, id=document_id)

    # Only the document owner can delete
    if document.owner != request.user:

        AuditLog.objects.create(
            actor=request.user,
            document=document,
            action='ACCESS_DENIED',
            details=f'Unauthorized deletion attempt for document: {document.title}',
            ip_address=request.META.get('REMOTE_ADDR')
        )

        return HttpResponseForbidden(
            'Access denied. Only the document owner can delete this document.'
        )

    # Preserve document information before deletion
    document_title = document.title
    document_category = document.category

    # Record deletion before removing the document
    AuditLog.objects.create(
        actor=request.user,
        document=document,
        action='DELETE',
        details=(
            f'Deleted document: {document_title}. '
            f'Category: {document_category}.'
        ),
        ip_address=request.META.get('REMOTE_ADDR')
    )

    # Delete the stored file
    if document.file:
        document.file.delete(save=False)

    document.delete()

    messages.success(request, 'Document deleted successfully!')
    return redirect('document_list')
