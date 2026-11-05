
import tempfile

from django.test import TestCase, override_settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from documents.models import Document, DocumentPermission
from documents.forms import DocumentForm
from audit.models import AuditLog


class DocumentSecurityTests(TestCase):

    def setUp(self):
        self.temp_media = tempfile.TemporaryDirectory()
        self.media_override = override_settings(
            MEDIA_ROOT=self.temp_media.name
        )
        self.media_override.enable()

        self.owner = User.objects.create_user(
            username='owner_test',
            password='Owner@12345'
        )

        self.viewer = User.objects.create_user(
            username='viewer_test',
            password='Viewer@12345'
        )

        self.unauthorized = User.objects.create_user(
            username='unauthorized_test',
            password='User@12345'
        )

        # Set the owner role
        self.owner.userprofile.role = 'OWNER'
        self.owner.userprofile.save()

        test_file = SimpleUploadedFile(
            'security_test.txt',
            b'This is a test document.',
            content_type='text/plain'
        )

        self.document = Document.objects.create(
            title='Security Test Document',
            category='Testing',
            owner=self.owner,
            file=test_file
        )

        self.permission = DocumentPermission.objects.create(
            document=self.document,
            user=self.viewer,
            permission='READ',
            granted_by=self.owner
        )

    def tearDown(self):
        self.media_override.disable()
        self.temp_media.cleanup()

    # TEST 1
    def test_owner_can_view_document_list(self):
        self.client.login(
            username='owner_test',
            password='Owner@12345'
        )

        response = self.client.get(reverse('document_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Security Test Document')

    # TEST 2
    def test_unauthorized_user_cannot_see_document(self):
        self.client.login(
            username='unauthorized_test',
            password='User@12345'
        )

        response = self.client.get(reverse('document_list'))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Security Test Document')

    # TEST 3
    def test_viewer_can_download_with_read_permission(self):
        self.client.login(
            username='viewer_test',
            password='Viewer@12345'
        )

        response = self.client.get(
            reverse('download_document', args=[self.document.id])
        )

        self.assertEqual(response.status_code, 200)
        response.close()

    # TEST 4
    def test_unauthorized_user_cannot_download(self):
        self.client.login(
            username='unauthorized_test',
            password='User@12345'
        )

        response = self.client.get(
            reverse('download_document', args=[self.document.id])
        )

        self.assertEqual(response.status_code, 403)

    # TEST 5
    def test_unauthorized_user_cannot_edit(self):
        self.client.login(
            username='unauthorized_test',
            password='User@12345'
        )

        response = self.client.get(
            reverse('edit_document', args=[self.document.id])
        )

        self.assertEqual(response.status_code, 403)

    # TEST 6
    def test_read_permission_cannot_edit(self):
        self.client.login(
            username='viewer_test',
            password='Viewer@12345'
        )

        response = self.client.get(
            reverse('edit_document', args=[self.document.id])
        )

        self.assertEqual(response.status_code, 403)

    # TEST 7
    def test_unauthorized_user_cannot_delete(self):
        self.client.login(
            username='unauthorized_test',
            password='User@12345'
        )

        response = self.client.post(
            reverse('delete_document', args=[self.document.id])
        )

        self.assertEqual(response.status_code, 403)

        self.assertTrue(
            Document.objects.filter(id=self.document.id).exists()
        )

    # TEST 8
    def test_revoked_user_cannot_download(self):
        self.permission.delete()

        self.client.login(
            username='viewer_test',
            password='Viewer@12345'
        )

        response = self.client.get(
            reverse('download_document', args=[self.document.id])
        )

        self.assertEqual(response.status_code, 403)

    # TEST 9
    def test_deleted_document_details_remain_in_audit_log(self):
        self.client.login(
            username='owner_test',
            password='Owner@12345'
        )

        response = self.client.post(
            reverse('delete_document', args=[self.document.id])
        )

        self.assertEqual(response.status_code, 302)

        audit = AuditLog.objects.get(
            action='DELETE',
            actor=self.owner
        )

        self.assertIn('Security Test Document', audit.details)
        self.assertIn('Testing', audit.details)
        self.assertIsNone(audit.document)

    # TEST 10
    def test_edit_permission_allows_editing(self):
        self.permission.permission = 'EDIT'
        self.permission.save()

        self.client.login(
            username='viewer_test',
            password='Viewer@12345'
        )

        response = self.client.get(
            reverse('edit_document', args=[self.document.id])
        )

        self.assertEqual(response.status_code, 200)

    # TEST 11
    def test_unauthorized_user_cannot_share(self):
        self.client.login(
            username='unauthorized_test',
            password='User@12345'
        )

        response = self.client.get(
            reverse('share_document', args=[self.document.id])
        )

        self.assertEqual(response.status_code, 403)

    # TEST 12
    def test_unauthorized_user_cannot_revoke_permission(self):
        self.client.login(
            username='unauthorized_test',
            password='User@12345'
        )

        response = self.client.post(
            reverse(
                'revoke_permission',
                args=[self.document.id, self.permission.id]
            )
        )

        self.assertEqual(response.status_code, 403)

        # Permission must still exist
        self.assertTrue(
            DocumentPermission.objects.filter(
                id=self.permission.id
            ).exists()
        )

        # Unauthorized attempt must be recorded
        self.assertTrue(
            AuditLog.objects.filter(
                actor=self.unauthorized,
                document=self.document,
                action='ACCESS_DENIED',
                details__icontains='revoke'
            ).exists()
        )

    # TEST 13
    def test_invalid_file_upload_is_rejected(self):
        invalid_file = SimpleUploadedFile(
            'malicious.exe',
            b'Invalid file content',
            content_type='application/octet-stream'
        )

        form = DocumentForm(
            data={
                'title': 'Invalid Document',
                'category': 'Testing'
            },
            files={
                'file': invalid_file
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn('file', form.errors)

    # TEST 14
    def test_shared_documents_page_shows_only_shared_documents(self):
        self.client.login(
            username='viewer_test',
            password='Viewer@12345'
        )

        response = self.client.get(
            reverse('shared_documents')
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Security Test Document')
