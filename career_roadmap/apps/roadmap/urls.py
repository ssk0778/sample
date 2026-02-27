from django.urls import path

from .views import ai_assessment_dashboard_view, assessment_view, dashboard_view, profile_setup_view

app_name = "roadmap"

urlpatterns = [
    path("", dashboard_view, name="dashboard"),
    path("profile/setup/", profile_setup_view, name="profile_setup"),
    path("assessment/", assessment_view, name="assessment"),
    path("assessment/ai/", ai_assessment_dashboard_view, name="ai_assessment_dashboard"),
]
