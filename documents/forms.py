
from django import forms
from django.contrib.auth.models import User
from pathlib import Path

from .models import Document, DocumentPermission

class DocumentForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = ['title', 'file', 'category']

        widgets = {
            'file': forms.FileInput(
                attrs={'class': 'form-control'}
            ),
        }

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')

        if not uploaded_file:
            return uploaded_file

        # Check allowed file extensions
        allowed_extensions = ['.pdf', '.doc', '.docx', '.txt']
        extension = Path(uploaded_file.name).suffix.lower()

        if extension not in allowed_extensions:
            raise forms.ValidationError(
                'Only PDF, DOC, DOCX and TXT files are allowed.'
            )

        # Check file size (maximum 10 MB)
        if uploaded_file.size > 10 * 1024 * 1024:
            raise forms.ValidationError(
                'File size must not exceed 10 MB.'
            )

        # Read the first bytes of the file
        file_header = uploaded_file.read(8)

        # Return the file pointer to the beginning
        uploaded_file.seek(0)

        # Validate file signatures
        if extension == '.pdf':
            if not file_header.startswith(b'%PDF-'):
                raise forms.ValidationError(
                    'Invalid PDF file.'
                )

        elif extension == '.doc':
            if not file_header.startswith(
                bytes.fromhex('D0CF11E0A1B11AE1')
            ):
                raise forms.ValidationError(
                    'Invalid DOC file.'
                )

        elif extension == '.docx':
            if not file_header.startswith(b'PK'):
                raise forms.ValidationError(
                    'Invalid DOCX file.'
                )

        elif extension == '.txt':
            try:
                uploaded_file.read().decode('utf-8')
            except UnicodeDecodeError:
                raise forms.ValidationError(
                    'Invalid text file. Please upload a UTF-8 text file.'
                )
            finally:
                uploaded_file.seek(0)

        return uploaded_file


class DocumentPermissionForm(forms.ModelForm):

    class Meta:
        model = DocumentPermission
        fields = ['user', 'permission']

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user', None)

        super().__init__(*args, **kwargs)

        users = User.objects.all()

        if current_user:
            users = users.exclude(id=current_user.id)

        self.fields['user'].queryset = users.order_by('username')
