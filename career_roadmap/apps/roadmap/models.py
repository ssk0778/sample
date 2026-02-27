from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class UserProfile(models.Model):
    EDUCATION_LEVEL_CHOICES = [
        ("high_school", "High School"),
        ("undergraduate", "Undergraduate"),
        ("postgraduate", "Postgraduate"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    current_education_level = models.CharField(max_length=20, choices=EDUCATION_LEVEL_CHOICES)
    preferred_domain = models.CharField(max_length=100)
    technical_skills = models.TextField(help_text="Comma-separated skills")
    career_goal = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user.username} Profile"


class StudentAssessment(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="assessments")
    aptitude_score = models.PositiveSmallIntegerField()
    communication_score = models.PositiveSmallIntegerField()
    coding_score = models.PositiveSmallIntegerField()
    leadership_score = models.PositiveSmallIntegerField()
    interests = models.TextField(help_text="Key interests, projects, and extracurricular activities")
    constraints = models.TextField(blank=True, help_text="Any location, financial, or schedule constraints")
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self) -> str:
        return f"Assessment #{self.pk} - {self.profile.user.username}"


class CareerRecommendation(models.Model):
    assessment = models.OneToOneField(StudentAssessment, on_delete=models.CASCADE, related_name="recommendation")
    recommended_roles = models.JSONField(default=list)
    learning_path = models.JSONField(default=list)
    roadmap_summary = models.TextField()
    confidence_score = models.DecimalField(max_digits=5, decimal_places=2)
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-generated_at"]

    def __str__(self) -> str:
        return f"Recommendation for assessment #{self.assessment_id}"


class StudentCareerAssessment(models.Model):
    class InterestChoices(models.TextChoices):
        AI_ML = "ai_ml", "AI / Machine Learning"
        WEB_DEVELOPMENT = "web_development", "Web Development"
        DATA_SCIENCE = "data_science", "Data Science"
        CYBER_SECURITY = "cyber_security", "Cyber Security"
        CLOUD_COMPUTING = "cloud_computing", "Cloud Computing"

    class SkillChoices(models.TextChoices):
        PYTHON = "python", "Python"
        JAVA = "java", "Java"
        JAVASCRIPT = "javascript", "JavaScript"
        SQL = "sql", "SQL"
        COMMUNICATION = "communication", "Communication"
        PROBLEM_SOLVING = "problem_solving", "Problem Solving"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="career_assessments")
    interests = models.JSONField(default=list, help_text="Select one or more interest areas")
    skills = models.JSONField(default=list, help_text="Select one or more current skills")
    strong_subjects = models.TextField(help_text="Core academic subjects the student performs well in")
    financial_background = models.CharField(max_length=150, help_text="e.g., low, middle, high income")
    career_goals = models.TextField(help_text="Long-term and short-term career aspirations")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Career Assessment #{self.pk} - {self.user.username}"

    def clean(self) -> None:
        super().clean()
        valid_interests = {choice for choice, _ in self.InterestChoices.choices}
        valid_skills = {choice for choice, _ in self.SkillChoices.choices}

        invalid_interests = [interest for interest in self.interests if interest not in valid_interests]
        invalid_skills = [skill for skill in self.skills if skill not in valid_skills]

        if invalid_interests:
            raise ValidationError({"interests": f"Invalid interests: {', '.join(invalid_interests)}"})

        if invalid_skills:
            raise ValidationError({"skills": f"Invalid skills: {', '.join(invalid_skills)}"})
