# TrustVault – Security Threat Model

## 1. Introduction

TrustVault is a secure document-sharing application developed using Django. It protects confidential documents through authentication, document-level permissions, private file storage and activity auditing.

This document identifies potential security threats, their impact and the measures implemented to reduce security risks.

## 2. Assets to Protect

The important assets in TrustVault are:

- User accounts and authentication information.
- Uploaded confidential documents.
- Document ownership information.
- Read and Edit permissions.
- User and document activity logs.
- Application configuration and secret keys.

## 3. Security Threats and Mitigations

### Threat 1: Unauthorized Document Access

**Risk:** A user may attempt to access documents that do not belong to them or have not been shared with them.

**Impact:** Confidential information could be exposed.

**Mitigation:**
- Verify user authentication before protected operations.
- Check document ownership and permissions before access.
- Restrict document access based on Read and Edit permissions.
- Record unauthorized access attempts in audit logs.

### Threat 2: Unauthorized Document Modification

**Risk:** A user with Read-only permission may attempt to modify a document.

**Impact:** Document integrity could be compromised.

**Mitigation:**
- Allow editing only to document owners and users with Edit permission.
- Validate authorization before processing document updates.
- Record successful modifications and denied attempts.

### Threat 3: Unauthorized Document Download

**Risk:** A user may try to download a document without permission.

**Impact:** Confidential files could be leaked.

**Mitigation:**
- Use a protected document download endpoint.
- Check the user's current permission for every download request.
- Record successful downloads and denied attempts.
- Avoid exposing uploaded files through public media URLs.

### Threat 4: Permission Misuse

**Risk:** Incorrect or unauthorized sharing permissions could expose confidential documents.

**Impact:** Sensitive documents may become accessible to unintended users.

**Mitigation:**
- Allow document owners to grant and revoke permissions.
- Support separate Read and Edit permissions.
- Check permissions before allowing document operations.
- Record permission changes in audit logs.

### Threat 5: Malicious File Upload

**Risk:** An attacker may upload an unsupported or invalid file.

**Impact:** Malicious or unexpected files could create security and storage risks.

**Mitigation:**
- Restrict supported file extensions.
- Enforce a maximum upload size.
- Validate file content using basic file signatures or content checks.
- Store uploaded files in private storage.

### Threat 6: Unauthorized Account Access

**Risk:** An attacker may attempt to access another user's account.

**Impact:** The attacker could access documents and perform actions using that account.

**Mitigation:**
- Use Django authentication and password-handling mechanisms.
- Require authentication for protected application operations.
- Associate document permissions with authenticated users.

### Threat 7: Audit Log Manipulation or Loss

**Risk:** Important activity records may be missing or improperly associated with users and documents.

**Impact:** Security investigations and accountability could be affected.

**Mitigation:**
- Maintain database-backed audit records.
- Record important actions such as uploads, downloads, updates, deletions, grants and revocations.
- Record unauthorized access attempts.
- Preserve audit history when a referenced document is deleted.

## 4. Security Testing

The application includes automated tests for important security scenarios.

The tested scenarios include:

- Users cannot view other users' private documents.
- Unauthorized users cannot download documents.
- Unauthorized users cannot edit or delete documents.
- Read-only users cannot modify documents.
- Revoked permissions prevent future access.
- Users with Edit permission can perform authorized operations.
- Unauthorized access attempts are recorded.
- Invalid file uploads are rejected.
- Audit history is preserved after document deletion.

## 5. Residual Risks and Future Improvements

Security is an ongoing process. The following areas require continued attention:

- Rate limiting and protection against repeated login attempts.
- Stronger file-content validation for uploaded document formats.
- Production HTTPS and secure cookie configuration.
- Database and private file backups.
- Monitoring and alerting for suspicious activity.
- Periodic security reviews and dependency updates.

## 6. Conclusion

TrustVault applies authentication, document-level authorization, private file storage, upload validation and audit logging to protect confidential documents.

The application is designed around three important security principles:

1. **Confidentiality:** Only authorized users can access documents.
2. **Integrity:** Only users with appropriate permissions can modify documents.
3. **Accountability:** Important activities and unauthorized attempts are recorded.

The security controls and tests help demonstrate the application's approach to secure document sharing.