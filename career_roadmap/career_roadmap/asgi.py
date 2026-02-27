"""ASGI config for career_roadmap project."""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "career_roadmap.settings")

application = get_asgi_application()
