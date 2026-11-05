# TrustVault – Secure Document Sharing with Audit Trail

## Project Overview

TrustVault is a secure document-sharing web application built with Django. It allows users to upload, manage, share and access documents through permission-based access control.

The application helps protect confidential documents by ensuring that users can only perform actions they are authorized to perform. It also maintains an audit trail of important document activities.

## Key Features

- **User Authentication:** User registration and login.
- **Role-Based Access:** Admin, Document Owner and Viewer roles.
- **Document Management:** Upload, organize, edit, search and manage documents.
- **Permission Management:** Grant or revoke Read and Edit permissions for individual documents.
- **Secure Downloads:** Check user permissions before allowing document downloads.
- **Private File Storage:** Uploaded documents are stored outside public web-accessible media paths.
- **Activity Tracking:** Record uploads, downloads, updates, deletions and permission changes.
- **Access Denial Logging:** Record unauthorized access attempts.
- **Document Search:** Search documents using available document details.

## User Roles

| Role | Responsibilities |
|---|---|
| Admin | Manage the application and review activity and permission logs. |
| Document Owner | Upload and manage owned documents and control sharing permissions. |
| Viewer | Access documents shared with them according to their permissions. |

## Technology Stack

- **Backend:** Python, Django
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite (local development)
- **Version Control:** Git and GitHub

## Security Features

- Authentication required for protected operations.
- Document-level Read and Edit permissions.
- Authorization checks before document access and downloads.
- Permission revocation to prevent future unauthorized access.
- Private document file storage.
- File extension, size and content validation.
- Audit logging for important document activities and denied access attempts.
- Sensitive configuration values are handled using environment variables.

## Project Structure

```text
TrustVault/
├── accounts/
├── audit/
├── config/
├── documents/
├── manage.py
├── .gitignore
└── README.md
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

Install the packages listed in the project's dependency file (`requirements.txt`), if available:

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Set the Django secret key and development settings using your own local environment values.

Do not publish secret keys or passwords in the repository.

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

## Running Tests

Run the automated Django test suite:

```bash
python manage.py test
```

## Project Objective

The main objective of TrustVault is to demonstrate secure document sharing through authentication, document-level authorization, private file storage and reliable activity auditing.

The project focuses on confidentiality, controlled access and accountability.

## Developer

**Ruksana Shaik**

GitHub: https://github.com/shaikruksana1328

---

*TrustVault – Your documents, your permissions, your security.*