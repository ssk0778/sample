# AI-Based Smart Career Roadmap Generator (Django)

## Folder Structure

```text
career_roadmap/
├── manage.py
├── requirements.txt
├── README.md
├── career_roadmap/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── templates/
│   └── registration/
│       └── login.html
└── apps/
    └── roadmap/
        ├── __init__.py
        ├── admin.py
        ├── apps.py
        ├── forms.py
        ├── models.py
        ├── urls.py
        ├── views.py
        ├── migrations/
        │   └── __init__.py
        ├── services/
        │   └── recommender.py
        └── templates/roadmap/
            ├── assessment_form.html
            ├── dashboard.html
            └── profile_setup.html
```

## Core Models

- `UserProfile`: stores education level, preferred domain, skills, and career goals.
- `StudentAssessment`: stores student self-evaluation scores and context.
- `CareerRecommendation`: stores AI-generated roles, learning path, summary, and confidence.

## URL Endpoints

- `GET/POST /accounts/login/` - login page
- `POST /accounts/logout/` - logout endpoint
- `GET /` - dashboard
- `GET/POST /profile/setup/` - profile setup
- `GET/POST /assessment/` - student assessment + recommendation generation

## Basic View Flow

1. User logs in.
2. User sets up `UserProfile`.
3. User submits `StudentAssessment`.
4. AI service (`generate_career_recommendation`) creates recommendation.
5. Dashboard displays personalized roadmap.

## Settings Highlights

- App registration: `apps.roadmap`
- SQLite default DB
- Template dirs at project-level and app-level
- Auth redirects:
  - `LOGIN_REDIRECT_URL = "roadmap:dashboard"`
  - `LOGIN_URL = "login"`
  - `LOGOUT_REDIRECT_URL = "login"`

## Run Locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
