# Rooted in Knowledge — The Sweet Root of Bustos

An interactive learning web app built with Django for exploring lessons about Minasa (arrowroot), taking quizzes, playing educational games, and viewing basic analytics.

## Key Features

### Student Side (Public + Logged-in Students)

**Public / Anonymous (no account needed):**
- Browse the homepage and lesson catalog
- View lesson content pages
- View and take quizzes
- Browse all games; **play the first 3 games** without logging in
- View the Festival Tour content

**Logged-in Students:**
- Account flows: sign up, login/logout, change password
- Profile dashboard:
	- recent activity timeline
	- quiz attempt history + summary stats
	- game attempt history + summary stats
	- best scores per game
- Profile management:
	- upload profile picture
	- update profile fields (name/grade/birthday)

**Quizzes (student experience):**
- Quiz list + quiz detail page
- Quiz submission provides per-question feedback + overall score
- Attempts are saved for authenticated users and shown in the profile

**Games (student experience):**
Supported game types:
- Word Scramble
- Drag & Drop (fill-in-the-blanks + legacy sorting format)
- Image Identification (uploaded question image + text choices, plus legacy option-based format)
- Memory Match (text-based and image-based grids)

For authenticated users:
- attempts are saved
- score/max score and history are shown in the profile

### Admin/Staff Side

This project includes **two** staff interfaces:

**1) Django Admin (`/admin/`)**
- Standard Django admin for managing models and reviewing records (including activity logs)

**2) Custom Admin Panel (`/admin-panel/`) (staff only)**
- Dashboard with summary metrics
- Lesson/Section management:
	- create/edit/delete lesson sections (EducationalSection)
	- manage section images and YouTube videos
- Media + moderation:
	- manage media assets
	- moderate content (approve/reject) records
- Quizzes management:
	- create/edit/delete quizzes
	- create/edit questions and answer choices
- Games management:
	- create/edit/delete games
	- manage questions (including uploads for image-based games)
	- stats/leaderboards pages for games
- User management:
	- list/add/edit/delete users (non-admin users)
- Reporting:
	- export visits CSV
	- export moderation CSV
	- export users CSV
- Admin analytics endpoints for charts:
	- visits JSON
	- top pages JSON

### Analytics + Activity Logging
- Visit tracking middleware records GET page visits (excluding `/static/` and `/media/`)
- Activity logging tracks authenticated user actions (login/logout, lesson views, quiz/game events, profile updates, etc.)

## Tech Stack
- Django + Django REST Framework
- SQLite (default)
- Tailwind (frontend styling)

## Project Structure
- `minasa_site/` — Django project settings + root URLs
- `core/` — public pages, lessons, festival tour, profiles, access control, custom admin panel
- `quizzes/` — quiz models + quiz UI + quiz API/submission
- `games/` — game models + gameplay UI + attempt tracking
- `templates/`, `static/`, `media/` — UI templates, static files, uploaded media

## Quick Start (Windows PowerShell)

1) Create venv + install dependencies

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2) Run migrations

```powershell
python manage.py migrate
```

3) Create an admin user (optional but recommended)

```powershell
python manage.py createsuperuser
```

4) Run the server

```powershell
python manage.py runserver
```

Open: http://127.0.0.1:8000/

## Important URLs
- Home: `/`
- Lessons: `/lessons/`
- Festival Tour: `/festival-tour/`
- Quizzes: `/quizzes/`
- Games: `/games/`
- Profile (login required): `/profile/`
- Django Admin: `/admin/`
- Custom Admin Panel (staff only): `/admin-panel/`

## Configuration

### Media Uploads
Uploads go to `media/` (served automatically in development when `DEBUG=True`).

### Email (SMTP)
Email sending is configurable via environment variables. Recommended approach for GitHub/production:
- keep credentials out of the repo
- set `DJANGO_EMAIL_BACKEND`, `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `DEFAULT_FROM_EMAIL` in your host/CI secrets