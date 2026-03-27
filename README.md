# Rooted in Knowledge — The Sweet Root of Bustos

An interactive learning web app built with Django for exploring lessons about Minasa (arrowroot), taking quizzes, playing educational games, and viewing basic analytics.

## Key Features

### Public Learning Access (No Account Needed)
- **Homepage** with featured lessons
- **Lessons**: browse and view lesson content
- **Quizzes**: view and take quizzes
- **Games**: browse all games; **play the first 3 games** without logging in
- **Festival Tour**: view the virtual tour content (some interactive actions are reserved for logged-in users)

### Student Accounts
- Sign up, login/logout, change password
- **Profile page** with:
	- recent activity timeline
	- quiz attempt history + stats
	- game attempt history + stats
	- profile picture upload
	- editable profile fields (name/grade/birthday)

### Quizzes
- Quiz list + quiz detail page
- JSON API endpoint for quiz data (used by the frontend)
- Quiz submission endpoint returning:
	- per-question correctness
	- score and percentage
- For authenticated users: quiz attempts are saved and shown in the profile

### Educational Games
Game types supported:
- **Word Scramble**
- **Drag & Drop** (fill-in-the-blanks and legacy sorting support)
- **Image Identification** (uploaded question image + text choices, plus legacy option-based format)
- **Memory Match** (text-based and image-based grids)

For authenticated users:
- game attempts are saved
- score, max score, and attempt history are shown in the profile

### Custom Admin Panel (Staff Only)
- Dashboard with summary metrics
- CRUD management for:
	- lesson sections (EducationalSection)
	- section images and YouTube videos
	- media assets and moderation records
	- quizzes and questions
	- games and questions (including image uploads)
	- users
- Exports:
	- visits CSV
	- moderation CSV
	- users CSV
- JSON endpoints for admin charts (visits + top pages)

### Analytics + Activity Logging
- **Visit tracking middleware** records GET page visits (excluding `/static/` and `/media/`)
- **Activity logging** tracks authenticated user actions (login/logout, lesson views, quiz/game start & completion, profile updates, etc.)

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

## Documentation
- See ACTIVITY_LOGGING_GUIDE.md for the activity log system
- See GAMES_IMPLEMENTATION.md for game types and admin setup
- See PUBLIC_ACCESS_IMPLEMENTATION.md for anonymous vs authenticated access rules

## Notes for Publishing to GitHub
- Do **not** commit real secrets (SMTP passwords, Django secret key). Use environment variables instead.
- If you plan to deploy, set `DEBUG=False`, configure `ALLOWED_HOSTS`, and use a production database.

