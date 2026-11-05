# TrustVault – Endpoint Documentation

## 1. Overview

TrustVault is a Django-based secure document-sharing application. It uses server-rendered web views and Django authentication to manage users, documents, permissions, and audit logs.

**Base URL (local development):** `http://127.0.0.1:8000/`

All protected endpoints require an authenticated user unless otherwise specified.

## 2. Authentication Endpoints

| Method | Endpoint | Description | Access |
|---|---|---|---|
| GET, POST | `/accounts/register/` | Register a new user | Public |
| GET, POST | `/accounts/login/` | Authenticate a user | Public |
| GET | `/accounts/dashboard/` | Display dashboard and statistics | Authenticated |
| POST | `/accounts/logout/` | Log out the current user | Authenticated |

## 3. Document Endpoints

| Method | Endpoint | Description | Access |
|---|---|---|---|
| GET | `/documents/` | List accessible documents and search/filter | Authenticated |
| GET | `/documents/shared/` | View documents shared with the current user | Authenticated |
| GET | `/documents/access-management/` | View permission management records | Document Owner |
| GET, POST | `/documents/upload/` | Upload a new document | Document Owner |
| GET | `/documents/<document_id>/download/` | Download a document | Owner, READ or EDIT |
| GET, POST | `/documents/<document_id>/share/` | Grant or update document permissions | Document Owner |
| POST | `/documents/<document_id>/revoke/<permission_id>/` | Revoke document permission | Document Owner |
| GET, POST | `/documents/<document_id>/edit/` | Edit document details or file | Owner or EDIT |
| POST | `/documents/<document_id>/delete/` | Delete a document | Document Owner |

## 4. Audit Endpoints

| Method | Endpoint | Description | Access |
|---|---|---|---|
| GET | `/audit/activity/` | View, search and filter activity logs | Administrator |

## 5. Authorization Rules

- Users must authenticate before accessing protected functionality.
- Document owners can manage their own documents.
- Users with READ permission can download documents but cannot edit them.
- Users with EDIT permission can download and edit documents.
- Only document owners can share documents or revoke permissions.
- Only document owners can delete their documents.
- Only administrators can access activity logs.
- Unauthorized document operations are blocked and recorded where implemented.
- Document access is checked on the server for each download request.

## 6. Audit Logging

TrustVault records the following activities:

- UPLOAD – Document uploaded.
- DOWNLOAD – Document downloaded.
- UPDATE – Document updated.
- DELETE – Document deleted.
- GRANT – Permission granted or updated.
- REVOKE – Permission revoked.
- ACCESS_DENIED – Unauthorized access attempt.

Audit records include the actor, document where applicable, target user where applicable, action, details, IP address where captured, and timestamp.

## 7. Request and Response Behaviour

TrustVault uses standard Django web requests and responses.

- GET requests display pages or retrieve permitted documents.
- POST requests submit forms or perform state-changing operations.
- Successful form submissions generally redirect to another page.
- Unauthorized operations return HTTP 403 Forbidden.
- Missing document or permission records return HTTP 404 Not Found.
- Login-protected pages redirect unauthenticated users to the login page.

## 8. Security Notes

- Django authentication protects restricted views.
- Document ownership and permission checks are performed in the views.
- Private document downloads use a protected Django view.
- Permission revocation removes the corresponding permission record.
- State-changing POST forms use Django's CSRF protection when submitted through the application templates.

## 9. Important Note

This project currently implements Django server-rendered web endpoints. It does not claim to provide a separate REST API or token-based API authentication.

