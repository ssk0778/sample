from django import forms

from .models import StudentAssessment, StudentCareerAssessment, UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "current_education_level",
            "preferred_domain",
            "technical_skills",
            "career_goal",
        ]


class StudentAssessmentForm(forms.ModelForm):
    class Meta:
        model = StudentAssessment
        fields = [
            "aptitude_score",
            "communication_score",
            "coding_score",
            "leadership_score",
            "interests",
            "constraints",
        ]
        widgets = {
            "aptitude_score": forms.NumberInput(attrs={"min": 0, "max": 100}),
            "communication_score": forms.NumberInput(attrs={"min": 0, "max": 100}),
            "coding_score": forms.NumberInput(attrs={"min": 0, "max": 100}),
            "leadership_score": forms.NumberInput(attrs={"min": 0, "max": 100}),
        }


class StudentCareerAssessmentForm(forms.ModelForm):
    interests = forms.MultipleChoiceField(
        choices=StudentCareerAssessment.InterestChoices.choices,
        widget=forms.CheckboxSelectMultiple,
    )
    skills = forms.MultipleChoiceField(
        choices=StudentCareerAssessment.SkillChoices.choices,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = StudentCareerAssessment
        fields = [
            "interests",
            "skills",
            "strong_subjects",
            "financial_background",
            "career_goals",
        ]
