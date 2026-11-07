# TrustVault – Secure Document Sharing with Audit Trail

## Project Overview

TrustVault is a secure document-sharing web application built with Python and Django. It allows users to upload, manage, share and access documents through role-based and document-level permission controls.

The application protects confidential documents by ensuring that users can only perform actions they are authorized to perform. It also maintains an audit trail of important document activities for accountability and monitoring.

## Live Application

**Live Website:** https://trustvault-zbyx.onrender.com

**GitHub Repository:** https://github.com/shaikruksana1328/TrustVault

## Key Features

- **User Authentication:** User registration, login and logout.
- **Role-Based Access Control:** Three roles – Admin, Document Owner and Viewer.
- **Document Management:** Upload, view, search, edit document details and delete documents.
- **Document Search and Filtering:** Search documents and filter them using available year and month options.
- **Permission Management:** Document owners can grant or revoke Read and Edit permissions for individual users.
- **Secure Downloads:** Check permissions before allowing users to download documents.
- **Private File Storage:** Store uploaded documents using private storage rather than public web-accessible media paths.
- **Activity Tracking:** Record important actions such as uploads, downloads, edits, deletions and permission changes.
- **Access Denial Logging:** Record unauthorized access attempts.
- **Admin Dashboard:** Display document statistics, download counts, shared-document counts and denied-access attempts.
- **Responsive Interface:** Pages are designed to work on desktop and mobile devices.

## User Roles

| Role | Responsibilities |
|---|---|
| Admin | Access the administrative dashboard and review activity logs. |
| Document Owner | Upload and manage owned documents, and grant or revoke sharing permissions. |
| Viewer | Access documents shared with them according to their assigned permissions. |

## Technology Stack

- **Backend:** Python, Django
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite for local development; deployment database configured through project settings.
- **File Storage:** Supabase Storage using its S3-compatible storage interface.
- **Local File Storage:** Django FileSystemStorage when Supabase storage is not enabled.
- **Version Control:** Git and GitHub
- **Deployment:** Render

## Storage Architecture

TrustVault uses Django to handle application logic, authentication, document permissions and database operations.

Uploaded document files are stored in a private Supabase Storage bucket when Supabase storage is enabled.

The configured bucket is:

`trustvault-documents`

Django manages access to the stored files and checks permissions before allowing protected document operations.

For local development, the application can use Django's local file storage when Supabase storage is disabled.

## Security Features

- Authentication required for protected operations.
- Role-based and document-level authorization.
- Separate Read and Edit permissions.
- Permission checks before document access and downloads.
- Permission revocation to prevent future unauthorized access.
- Private document storage.
- File validation, including supported file types and size restrictions.
- Audit logging for important document activities.
- Logging of unauthorized access attempts.
- Sensitive configuration values handled through environment variables.

## Project Structure

```text
TrustVault/
├── accounts/
├── audit/
├── config/
├── documents/
├── manage.py
├── requirements.txt
├── .gitignore
├── README.md
├── PROMPTS.md
├── THREATS.md
└── ENDPOINT_DOCUMENTATION.md
```

## Local Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/shaikruksana1328/TrustVault.git
cd TrustVault
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Configure the required environment variables according to the project's settings.

For local development, use your own Django secret key and appropriate development settings.

If using Supabase Storage, configure the required Supabase storage credentials and bucket settings.

Do not commit secret keys, passwords or storage credentials to GitHub.

### 6. Apply database migrations

```bash
python manage.py migrate
```

### 7. Create an administrator account

```bash
python manage.py createsuperuser
```

### 8. Start the development server

```bash
python manage.py runserver
```

Open the application at:

http://127.0.0.1:8000/

## Running Automated Tests

Run the Django test suite using:

```bash
python manage.py test
```

## Project Objective

The main objective of TrustVault is to demonstrate secure document sharing through authentication, role-based access control, document-level permissions, private file storage and activity auditing.

The project focuses on confidentiality, controlled access and accountability.

## Developer

**Ruksana Shaik**

GitHub: https://github.com/shaikruksana1328

---

*TrustVault – Your documents, your permissions, your security.*
