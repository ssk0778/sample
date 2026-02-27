from django.contrib import admin

from .models import CareerRecommendation, StudentAssessment, StudentCareerAssessment, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "current_education_level", "preferred_domain", "career_goal")
    search_fields = ("user__username", "preferred_domain", "career_goal")


@admin.register(StudentAssessment)
class StudentAssessmentAdmin(admin.ModelAdmin):
    list_display = ("profile", "aptitude_score", "coding_score", "submitted_at")
    list_filter = ("submitted_at",)


@admin.register(CareerRecommendation)
class CareerRecommendationAdmin(admin.ModelAdmin):
    list_display = ("assessment", "confidence_score", "generated_at")


@admin.register(StudentCareerAssessment)
class StudentCareerAssessmentAdmin(admin.ModelAdmin):
    list_display = ("user", "financial_background", "created_at")
    list_filter = ("financial_background", "created_at")
    search_fields = ("user__username", "strong_subjects", "career_goals")
