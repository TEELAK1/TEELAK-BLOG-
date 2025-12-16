# Blogmota – Personal Blog Platform

A full-stack personal blog platform built with Django, following a clean MVT architecture.

## Features

- CRUD for blog posts with rich-text content (CKEditor)
- Categories and tags
- Featured images and publish scheduling
- Draft/Published status
- Comments linked to posts and users
- Full Django authentication (register, login, logout)
- Admin-only content management
- Site-wide search (title, content, categories, tags)

## Getting Started (Development)

1. **Create and activate a virtual environment** (recommended).
2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Apply migrations**:

   ```bash
   python manage.py migrate
   ```

4. **Create a superuser** (admin account):

   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server**:

   ```bash
   python manage.py runserver
   ```

6. Visit `http://127.0.0.1:8000/` for the blog and `http://127.0.0.1:8000/admin/` for the Django admin.

## Rich Text Editing

This project uses **django-ckeditor** for rich text editing of post content. Ensure static and media files are configured as in `settings.py` and that you run `collectstatic` in production.

## Production Notes (High Level)

- Use **PostgreSQL** instead of SQLite by updating `DATABASES` in `blogmota/settings.py`.
- Run behind a WSGI/ASGI server such as **Gunicorn** and a reverse proxy like **Nginx**.
- Configure environment variables for `SECRET_KEY`, database credentials, and `DEBUG`.
- Serve static and media files from a dedicated storage (e.g., S3, CDN, or Nginx).
