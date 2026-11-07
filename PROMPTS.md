# TrustVault – AI Prompt Documentation

This document records representative AI prompts used during the development of TrustVault. AI assistance was used to understand project requirements, plan implementation, improve the user interface, review security practices, debug issues, test functionality and prepare project documentation.

## 1. Project Planning and Architecture

**Prompt:**

"Help me plan a secure document-sharing web application using Django. The application should support three roles: Admin, Document Owner and Viewer. Include document upload, document management, sharing permissions, access control and audit logging."

## 2. Authentication and Authorization

**Prompt:**

"Help implement and review Django authentication and role-based authorization. Ensure that only authorized users can access documents and perform actions according to their assigned roles and document permissions."

## 3. Document Management

**Prompt:**

"Help implement document upload, listing, search, date filtering, editing, deletion and downloading in Django. Ensure that document operations are restricted to authorized users and uploaded files are validated."

## 4. Permission Management

**Prompt:**

"Help implement document-level Read and Edit permissions. Document owners should be able to grant and revoke access to specific users. Ensure that permission changes are enforced when users attempt to access documents."

## 5. Audit Logging

**Prompt:**

"Help implement an audit logging system that records document uploads, downloads, edits, deletions, permission grants, permission revocations and unauthorized access attempts. Include the acting user, document and relevant activity details."

## 6. Private File Storage and Supabase Integration

**Prompt:**

"Help configure Django to use Supabase Storage through its S3-compatible interface. Keep uploaded documents private and ensure that authorized document operations can access stored files securely."

## 7. Debugging and Error Handling

**Prompt:**

"Help investigate Django and deployment errors using the actual error messages and application logs. Identify the root cause and suggest the smallest safe correction without breaking existing functionality."

## 8. User Interface and Responsive Design

**Prompt:**

"Improve the TrustVault interface with a consistent, modern and professional design across the Dashboard, My Documents, Shared With Me, Access Management, Activity Logs, Upload Document and Login/Registration pages. Maintain consistent navigation, typography, colors and light/dark themes while preserving existing Django functionality."

## 9. Mobile Responsiveness

**Prompt:**

"Review the TrustVault pages on mobile screens. Improve navigation, page layouts, buttons and sign-out accessibility. Ensure the mobile interface works correctly without affecting the desktop design."

## 10. Security Testing and Debugging

**Prompt:**

"Help identify and test security issues in the Django application. Check role-based access, document permissions, unauthorized downloads, permission revocation, document deletion and audit logging. Preserve existing security checks while fixing identified issues."

## 11. Deployment and Documentation

**Prompt:**

"Help prepare the Django application for deployment on Render and maintain its GitHub repository. Review the README, AI prompt documentation, threat documentation and endpoint documentation so they accurately describe the implemented application."

## Responsible Use of AI

AI assistance was used as a development aid throughout the project. Suggestions and generated code were reviewed, adapted and tested before being incorporated into TrustVault.

AI was particularly useful for understanding Django concepts, improving the user interface, debugging storage and deployment issues, and preparing documentation.

Development decisions were checked against the actual application, and implemented functionality was manually tested to verify expected behavior.