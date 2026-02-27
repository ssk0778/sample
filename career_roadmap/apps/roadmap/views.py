from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import StudentAssessmentForm, StudentCareerAssessmentForm, UserProfileForm
from .models import CareerRecommendation, StudentAssessment, StudentCareerAssessment, UserProfile
from .services.ai_engine import generate_recommendations
from .services.recommender import generate_career_recommendation


@login_required
def dashboard_view(request):
    profile = UserProfile.objects.filter(user=request.user).first()
    latest_assessment = StudentAssessment.objects.filter(profile=profile).first() if profile else None
    recommendation = (
        CareerRecommendation.objects.filter(assessment=latest_assessment).first()
        if latest_assessment
        else None
    )
    return render(
        request,
        "roadmap/dashboard.html",
        {
            "profile": profile,
            "latest_assessment": latest_assessment,
            "recommendation": recommendation,
        },
    )


@login_required
def profile_setup_view(request):
    profile, _ = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={
            "current_education_level": "undergraduate",
            "preferred_domain": "AI/ML",
            "technical_skills": "Python",
            "career_goal": "Become an AI Engineer",
        },
    )

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("roadmap:assessment")
    else:
        form = UserProfileForm(instance=profile)

    return render(request, "roadmap/profile_setup.html", {"form": form})


@login_required
def assessment_view(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == "POST":
        form = StudentAssessmentForm(request.POST)
        if form.is_valid():
            assessment = form.save(commit=False)
            assessment.profile = profile
            assessment.save()

            recommendation_data = generate_career_recommendation(assessment)
            CareerRecommendation.objects.update_or_create(
                assessment=assessment,
                defaults={
                    "recommended_roles": recommendation_data.recommended_roles,
                    "learning_path": recommendation_data.learning_path,
                    "roadmap_summary": recommendation_data.roadmap_summary,
                    "confidence_score": recommendation_data.confidence_score,
                },
            )
            return redirect("roadmap:dashboard")
    else:
        form = StudentAssessmentForm()

    return render(request, "roadmap/assessment_form.html", {"form": form})


@login_required
def ai_assessment_dashboard_view(request):
    """Collect student assessment, call ai_engine, save recommendation, and render dashboard."""
    profile, _ = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={
            "current_education_level": "undergraduate",
            "preferred_domain": "Technology",
            "technical_skills": "",
            "career_goal": "",
        },
    )

    if request.method == "POST":
        form = StudentCareerAssessmentForm(request.POST)
        if form.is_valid():
            career_assessment: StudentCareerAssessment = form.save(commit=False)
            career_assessment.user = request.user
            career_assessment.save()

            ai_output = generate_recommendations(career_assessment)
            top_recommendations = ai_output.get("top_3_recommendations", [])

            synthetic_assessment = StudentAssessment.objects.create(
                profile=profile,
                aptitude_score=75,
                communication_score=70,
                coding_score=75,
                leadership_score=68,
                interests=", ".join(career_assessment.interests),
                constraints=f"Financial background: {career_assessment.financial_background}",
            )

            primary = top_recommendations[0] if top_recommendations else {}
            learning_path = primary.get("four_year_roadmap", [])
            recommended_roles = [item.get("career") for item in top_recommendations if item.get("career")]
            reasoning_text = "\n".join(
                [f"{item.get('career')}: {item.get('reasoning')}" for item in top_recommendations]
            )

            recommendation = CareerRecommendation.objects.create(
                assessment=synthetic_assessment,
                recommended_roles=recommended_roles,
                learning_path=learning_path,
                roadmap_summary=reasoning_text,
                confidence_score=primary.get("match_score", 70),
            )

            return render(
                request,
                "roadmap/dashboard.html",
                {
                    "profile": profile,
                    "latest_assessment": synthetic_assessment,
                    "recommendation": recommendation,
                    "ai_output": ai_output,
                },
            )
    else:
        form = StudentCareerAssessmentForm()

    return render(request, "roadmap/assessment_form.html", {"form": form})
