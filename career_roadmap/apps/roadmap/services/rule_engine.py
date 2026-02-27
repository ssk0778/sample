"""Rule-based AI engine for recommending career paths.

The engine accepts student profile signals and returns a structured JSON payload:
- top 3 recommendations
- reasoning
- estimated salary range in India
- 4-year roadmap
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CareerRule:
    career: str
    base_reasoning: str
    salary_range_india: str
    roadmap: list[str]
    base_score: int


INTEREST_ROLE_MAP: dict[str, list[CareerRule]] = {
    "ai_ml": [
        CareerRule(
            career="Machine Learning Engineer",
            base_reasoning="Strong fit for students interested in AI systems and model-driven products.",
            salary_range_india="₹8L - ₹28L",
            roadmap=[
                "Year 1: Build Python, statistics, and linear algebra foundations.",
                "Year 2: Learn ML algorithms, SQL, and data engineering basics.",
                "Year 3: Create NLP/CV projects, deploy models, and complete internships.",
                "Year 4: Specialize in GenAI/MLOps and prepare for product-scale ML roles.",
            ],
            base_score=84,
        ),
        CareerRule(
            career="Data Scientist",
            base_reasoning="Suitable for analytical problem-solving and data storytelling roles.",
            salary_range_india="₹7L - ₹24L",
            roadmap=[
                "Year 1: Strengthen Python, probability, and Excel/BI tools.",
                "Year 2: Learn feature engineering, experimentation, and SQL at depth.",
                "Year 3: Build domain case studies and predictive modeling portfolio.",
                "Year 4: Focus on business-impact projects and advanced ML deployment.",
            ],
            base_score=80,
        ),
    ],
    "web_development": [
        CareerRule(
            career="Full Stack Developer",
            base_reasoning="Ideal for building end-to-end web applications and product features.",
            salary_range_india="₹6L - ₹20L",
            roadmap=[
                "Year 1: Learn HTML/CSS/JavaScript and programming fundamentals.",
                "Year 2: Master backend frameworks, APIs, and relational databases.",
                "Year 3: Build scalable full-stack projects and complete internships.",
                "Year 4: Focus on system design, cloud deployment, and production readiness.",
            ],
            base_score=78,
        ),
        CareerRule(
            career="Frontend Engineer",
            base_reasoning="Great fit for UI-focused students with design and UX sensibilities.",
            salary_range_india="₹5L - ₹18L",
            roadmap=[
                "Year 1: Build strong fundamentals in web markup and JavaScript.",
                "Year 2: Learn React/Vue, state management, and testing.",
                "Year 3: Optimize performance, accessibility, and design systems.",
                "Year 4: Build advanced frontend architecture and mentoring capability.",
            ],
            base_score=74,
        ),
    ],
    "data_science": [
        CareerRule(
            career="Data Analyst",
            base_reasoning="A practical pathway for students who enjoy deriving insights from datasets.",
            salary_range_india="₹4L - ₹12L",
            roadmap=[
                "Year 1: Build spreadsheet analysis, SQL, and visualization basics.",
                "Year 2: Learn statistics, dashboarding, and reporting automation.",
                "Year 3: Work on business case studies and stakeholder communication.",
                "Year 4: Progress into advanced analytics and predictive insights.",
            ],
            base_score=72,
        ),
        CareerRule(
            career="Business Intelligence Engineer",
            base_reasoning="Strong option for students balancing technical analytics with business impact.",
            salary_range_india="₹7L - ₹18L",
            roadmap=[
                "Year 1: Strengthen SQL, data modeling, and spreadsheet workflows.",
                "Year 2: Learn BI tools (Power BI/Tableau) and warehouse concepts.",
                "Year 3: Build KPI frameworks and automate executive dashboards.",
                "Year 4: Design enterprise analytics architecture and governance.",
            ],
            base_score=75,
        ),
    ],
}

SKILL_MULTIPLIER = {
    "beginner": 0.92,
    "intermediate": 1.0,
    "advanced": 1.08,
}

SUBJECT_BONUS = {
    "mathematics": {"Machine Learning Engineer", "Data Scientist", "Data Analyst"},
    "computer science": {"Machine Learning Engineer", "Full Stack Developer", "Frontend Engineer"},
    "statistics": {"Data Scientist", "Data Analyst", "Business Intelligence Engineer"},
    "economics": {"Business Intelligence Engineer", "Data Analyst"},
}

FINANCIAL_PRIORITIES = {
    "low": "Includes scholarship-friendly certifications, open-source learning paths, and early internship strategy.",
    "middle": "Balances affordable certifications, internship preparation, and selective paid specialization.",
    "high": "Includes premium specialization options, global certifications, and international project exposure.",
}


DEFAULT_CAREERS = [
    CareerRule(
        career="Software Engineer",
        base_reasoning="Broad and resilient technology pathway with high demand across domains.",
        salary_range_india="₹6L - ₹22L",
        roadmap=[
            "Year 1: Learn programming fundamentals and problem solving.",
            "Year 2: Build backend/frontend strengths and database skills.",
            "Year 3: Gain real-world experience with internships and projects.",
            "Year 4: Prepare for placement with DSA, system design, and mock interviews.",
        ],
        base_score=70,
    ),
    CareerRule(
        career="Data Analyst",
        base_reasoning="Accessible analytics-focused role with clear upskilling progression.",
        salary_range_india="₹4L - ₹12L",
        roadmap=[
            "Year 1: Build data handling with spreadsheets and SQL.",
            "Year 2: Learn dashboards and exploratory data analysis.",
            "Year 3: Build portfolio projects from public datasets.",
            "Year 4: Prepare for analytics interviews and domain specialization.",
        ],
        base_score=68,
    ),
    CareerRule(
        career="Full Stack Developer",
        base_reasoning="Strong path for students interested in creating full web products.",
        salary_range_india="₹6L - ₹20L",
        roadmap=[
            "Year 1: Learn web fundamentals and programming basics.",
            "Year 2: Build APIs, authentication, and database-backed apps.",
            "Year 3: Deploy production-grade projects and contribute to open source.",
            "Year 4: Practice architecture, scalability, and interview readiness.",
        ],
        base_score=69,
    ),
]


def _normalize(value: str) -> str:
    return value.strip().lower().replace("-", "_")


def recommend_career_paths(payload: dict) -> dict:
    """Return top 3 career recommendations as structured JSON-compatible dict.

    Input payload keys:
    - interest (str)
    - skill_level (str: beginner/intermediate/advanced)
    - subject_strengths (list[str])
    - financial_background (str: low/middle/high)
    """

    interest = _normalize(payload.get("interest", ""))
    skill_level = _normalize(payload.get("skill_level", "intermediate"))
    subject_strengths = [_normalize(s) for s in payload.get("subject_strengths", [])]
    financial_background = _normalize(payload.get("financial_background", "middle"))

    candidates = INTEREST_ROLE_MAP.get(interest, DEFAULT_CAREERS)
    multiplier = SKILL_MULTIPLIER.get(skill_level, 1.0)
    finance_note = FINANCIAL_PRIORITIES.get(financial_background, FINANCIAL_PRIORITIES["middle"])

    ranked = []
    for rule in candidates:
        score = int(rule.base_score * multiplier)
        matched_subjects = []

        for subject in subject_strengths:
            if subject in SUBJECT_BONUS and rule.career in SUBJECT_BONUS[subject]:
                score += 4
                matched_subjects.append(subject)

        ranked.append((score, matched_subjects, rule))

    ranked.sort(key=lambda item: item[0], reverse=True)

    top_three = []
    for score, matched_subjects, rule in ranked[:3]:
        subject_reason = (
            f"Subject alignment found in: {', '.join(matched_subjects)}."
            if matched_subjects
            else "General domain alignment used due to limited subject overlap."
        )
        top_three.append(
            {
                "career": rule.career,
                "reasoning": f"{rule.base_reasoning} {subject_reason} {finance_note}",
                "estimated_salary_range_india": rule.salary_range_india,
                "four_year_roadmap": rule.roadmap,
                "match_score": score,
            }
        )

    return {
        "input": {
            "interest": interest,
            "skill_level": skill_level,
            "subject_strengths": subject_strengths,
            "financial_background": financial_background,
        },
        "top_3_recommendations": top_three,
    }
