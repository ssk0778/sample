"""AI engine integration layer for student career assessments."""

from __future__ import annotations

from apps.roadmap.services.rule_engine import recommend_career_paths


def _infer_skill_level(skills: list[str]) -> str:
    skill_count = len(skills)
    if skill_count <= 1:
        return "beginner"
    if skill_count <= 3:
        return "intermediate"
    return "advanced"


def generate_recommendations(student_assessment) -> dict:
    """Build AI-engine input from student assessment and return structured JSON output."""
    interest = student_assessment.interests[0] if student_assessment.interests else ""
    subject_strengths = [subject.strip() for subject in student_assessment.strong_subjects.split(",") if subject.strip()]

    payload = {
        "interest": interest,
        "skill_level": _infer_skill_level(student_assessment.skills),
        "subject_strengths": subject_strengths,
        "financial_background": student_assessment.financial_background,
    }
    return recommend_career_paths(payload)
