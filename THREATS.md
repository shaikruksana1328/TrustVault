# TrustVault – Security Threat Model

## 1. Introduction

TrustVault is a secure document-sharing web application developed using Python and Django. It protects confidential documents through authentication, role-based access control, document-level permissions, private file storage and activity auditing.

This document identifies potential security threats, their impact and the security measures implemented to reduce risks.

## 2. Assets to Protect

The important assets in TrustVault are:

- User accounts and authentication information.
- Uploaded confidential documents.
- Document ownership information.
- Read and Edit permissions.
- User and document activity logs.
- Application configuration and secret keys.
- Private file storage credentials.

## 3. Security Threats and Mitigations

### Threat 1: Unauthorized Document Access

**Risk:** A user may attempt to access documents that do not belong to them or have not been shared with them.

**Impact:** Confidential information could be exposed.

**Mitigation:**
- Require authentication for protected operations.
- Check document ownership and permissions before access.
- Restrict document access according to Read and Edit permissions.
- Record unauthorized access attempts in audit logs.

### Threat 2: Unauthorized Document Modification

**Risk:** A user with Read-only permission may attempt to modify document details.

**Impact:** Document information and integrity could be compromised.

**Mitigation:**
- Allow editing only to document owners and users with Edit permission.
- Validate authorization before processing document updates.
- Record successful modifications and denied attempts.

### Threat 3: Unauthorized Document Download

**Risk:** A user may try to download a document without permission.

**Impact:** Confidential files could be exposed.

**Mitigation:**
- Use a protected document download endpoint.
- Check the user's current permission for every download request.
- Record successful downloads and denied attempts.
- Store uploaded files in private storage instead of exposing them through public media URLs.

### Threat 4: Permission Misuse

**Risk:** Incorrect or unauthorized sharing permissions could expose confidential documents.

**Impact:** Sensitive documents may become accessible to unintended users.

**Mitigation:**
- Allow document owners to grant and revoke permissions.
- Support separate Read and Edit permissions.
- Check permissions before allowing protected document operations.
- Record permission changes in audit logs.
- Enforce revoked permissions on subsequent access requests.

### Threat 5: Malicious or Invalid File Upload

**Risk:** An attacker may attempt to upload unsupported, oversized or invalid files.

**Impact:** Malicious or unexpected files could create security and storage risks.

**Mitigation:**
- Restrict supported file types.
- Enforce file-size restrictions.
- Validate uploaded files through the application's upload validation.
- Store uploaded documents in private storage.

### Threat 6: Unauthorized Account Access

**Risk:** An attacker may attempt to access another user's account.

**Impact:** The attacker could access documents and perform actions using that account.

**Mitigation:**
- Use Django authentication and password-handling mechanisms.
- Require authentication for protected application operations.
- Associate document permissions with authenticated users.
- Keep sensitive configuration values outside publicly accessible source code.

### Threat 7: Audit Log Manipulation or Loss

**Risk:** Important activity records may be missing or improperly associated with users and documents.

**Impact:** Security investigations and accountability could be affected.

**Mitigation:**
- Maintain database-backed audit records.
- Record important actions such as uploads, downloads, edits, deletions, grants and revocations.
- Record unauthorized access attempts.
- Verify audit records for important document activities.
- Preserve relevant audit history when documents are deleted.

## 4. Security Testing and Verification

The application was manually tested through the deployed TrustVault website to verify important security and permission scenarios.

The verified scenarios include:

- Users cannot access documents that have not been shared with them.
- Unauthorized document downloads are restricted.
- Unauthorized sharing and revocation attempts are blocked.
- Read-only users cannot use the Edit option.
- Revoked permissions remove the document from the viewer's shared-document list and prevent subsequent access.
- Users with Edit permission can edit authorized document details.
- Important activities are recorded in Activity Logs.
- Upload, download, edit, delete, grant, revoke and access-denial audit records were checked.
- The document deletion and download records were verified.
- Dashboard statistics were compared with the corresponding audit records.

These checks demonstrate the application's implemented security controls. They do not represent an exhaustive penetration test or independent security audit.

## 5. Residual Risks and Future Improvements

Security is an ongoing process. The following areas require continued attention:

- Rate limiting and protection against repeated login attempts.
- Stronger file-content validation for uploaded document formats.
- Production HTTPS and secure cookie configuration reviews.
- Database and private file backups.
- Monitoring and alerting for suspicious activity.
- Periodic security reviews and dependency updates.
- Additional automated security and edge-case testing.

## 6. Conclusion

TrustVault applies authentication, role-based access control, document-level authorization, private file storage, upload validation and audit logging to protect confidential documents.

The application focuses on three important security principles:

1. **Confidentiality:** Only authorized users can access documents.
2. **Integrity:** Only users with appropriate permissions can modify document details.
3. **Accountability:** Important activities and unauthorized access attempts are recorded.

The implemented security controls and manual verification help demonstrate a practical approach to secure document sharing.