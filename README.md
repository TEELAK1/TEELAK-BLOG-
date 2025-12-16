# Blogmota Deployment Documentation

## 1. Project Architecture & Stack
- **Framework**: Django 5.x (Python)
- **Database**: 
  - **Development**: SQLite (local)
  - **Production**: PostgreSQL (managed by Render)
- **Frontend**: Bootstrap 5, FontAwesome, Custom CSS
- **Deployment Platform**: Render.com
- **Static Files**: Served via WhiteNoise

## 2. Security Implementation
- **SSL/HTTPS**: Enforced via Django settings (`SECURE_SSL_REDIRECT`).
- **Secret Management**: `SECRET_KEY` and `DEBUG` mode managed via Environment Variables.
- **Headers**: HSTS, XSS Protection, and Content-Type sniffing protection enabled.
- **Database**: Connection strings configured via `dj-database-url`.
- **RBAC**: Custom permissions ensuring users can only edit their own content.

## 3. Deployment Steps
1. **Push to GitHub**: Ensure the latest code is on the main branch.
2. **Render Dashboard**:
   - Create a new **Blueprint**.
   - Connect your GitHub repository.
   - Render will read `render.yaml` and automatically provision the Service and Database.
   - Click **Apply**.
3. **Verification**: Once deployed, visit the provided `.onrender.com` URL.

## 4. Updates & Maintenance
- **Update Process**:
  1. Make changes locally.
  2. Test via `python manage.py runserver`.
  3. Commit and push: `git push origin main`.
  4. Render will auto-deploy the new commit.
- **Database Backups**:
  - Render performs automatic daily backups for managed PostgreSQL databases.
  - Manual backups can be triggered from the Render Dashboard.

## 5. Logs & Monitoring
- Logs are available in the **Render Dashboard** under the "Logs" tab of the web service.
- Django errors are configured to print to `stdout` for easy monitoring.

## 6. Future Improvements
- **Media Storage**: Integrate AWS S3 for persistent user media uploads (currently ephemeral).
- **Email Service**: Configure SMTP (SendGrid/Mailgun) for password resets and email notifications.
