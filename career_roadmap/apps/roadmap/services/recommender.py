from dataclasses import dataclass

from apps.roadmap.models import StudentAssessment


@dataclass
class RecommendationResult:
    recommended_roles: list[str]
    learning_path: list[str]
    roadmap_summary: str
    confidence_score: float


def generate_career_recommendation(assessment: StudentAssessment) -> RecommendationResult:
    """Placeholder for AI/LLM recommendation logic."""
    avg_score = (
        assessment.aptitude_score
        + assessment.communication_score
        + assessment.coding_score
        + assessment.leadership_score
    ) / 4

    if assessment.coding_score >= 75:
        roles = ["Software Engineer", "Machine Learning Engineer", "Data Engineer"]
        learning_path = [
            "Strengthen Data Structures & Algorithms",
            "Build 2 AI/ML portfolio projects",
            "Contribute to open-source AI repos",
            "Apply for internships with mentorship",
        ]
    else:
        roles = ["Business Analyst", "Product Analyst", "Technical Recruiter"]
        learning_path = [
            "Improve analytical reasoning",
            "Learn SQL and dashboarding tools",
            "Develop communication and stakeholder management",
            "Build case-study portfolio",
        ]

    summary = (
        f"Based on your scores and interests ({assessment.interests[:80]}...), "
        "this roadmap prioritizes foundational growth, role discovery, and structured project work."
    )

    return RecommendationResult(
        recommended_roles=roles,
        learning_path=learning_path,
        roadmap_summary=summary,
        confidence_score=round(min(max(avg_score, 40), 95), 2),
    )
