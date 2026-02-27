"""WSGI config for career_roadmap project."""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "career_roadmap.settings")

application = get_wsgi_application()
