# Rooted in Knowledge — The Sweet Root of Bustos — Learning Site (Django skeleton)

This repository contains a minimal Django project skeleton for "Rooted in Knowledge — The Sweet Root of Bustos" — an interactive learning portal prototype focused on lessons, a festival tour, quizzes, and teacher analytics placeholders.

What is included
- Minimal Django project: `minasa_site`
- Two apps: `core` (pages, articles, festival tour), `quizzes` (quiz models + JSON endpoint placeholder)
- HTML templates (Tailwind via CDN, Alpine.js, AOS.js, Chart.js placeholders)
- `requirements.txt`

Quick start (Windows PowerShell 5.1)

1) Create a virtual environment and install requirements

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt
```

2) Run migrations and start server

```powershell
python manage.py migrate; python manage.py runserver
```

3) Open http://127.0.0.1:8000/

Notes
- This is a starting point with templates and placeholder views you can extend. Add media files (videos, PDFs) via Django admin when ready.

SMTP configuration & testing
---------------------------

This project defaults to the console email backend for development (emails are printed to the server console).

To enable real SMTP delivery in a safe way, set environment variables (for example via a `.env` file loaded by your process manager or via your hosting provider's secret manager).

Required variables (examples in `.env.example`):

- `DJANGO_EMAIL_BACKEND`: set to `django.core.mail.backends.smtp.EmailBackend` to use SMTP.
- `SMTP_HOST` / `SMTP_PORT`: your SMTP server and port (e.g. `smtp.mailtrap.io`, `587`).
- `SMTP_USER` / `SMTP_PASSWORD`: SMTP credentials.
- `SMTP_USE_TLS` / `SMTP_USE_SSL`: booleans (e.g. `True`/`False`).
- `DEFAULT_FROM_EMAIL`: sender address used by `send_mail`.

Don't commit real credentials to the repository. Use `.env.example` as a template and keep secrets out of version control.

Quick test (once environment variables are set):

1. Run migrations and start a shell or just run the management command to test email delivery:

```powershell
python manage.py send_test_email --to your.email@example.com
```

2. The command will attempt to send a simple test message and print success or an error. If you kept the default console backend, the message will be printed to your runserver console instead of being delivered.

Testing with a sandbox SMTP provider
-----------------------------------

If you don't want to use a real production SMTP account while testing, use a sandbox/testing provider such as Mailtrap or Ethereal (Ethereal accounts are ephemeral). Configure the SMTP vars to the values provided by the sandbox provider and run the `send_test_email` command.

