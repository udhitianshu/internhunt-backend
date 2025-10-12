from fastapi import APIRouter
from app.models.user_model import UserProfile
from app.utils.helpers import clean_text

router = APIRouter(prefix="/api", tags=["InternHunt"])

@router.get("/test")
def test_route():
    return {"message": "Routes are working fine ✅"}

@router.post("/profile")
def create_profile(user: UserProfile):
    """Accepts user profile data and returns cleaned info."""
    cleaned_skills = [clean_text(skill) for skill in user.skills]
    return {
        "name": user.name,
        "branch": user.branch,
        "skills": cleaned_skills,
        "status": "Profile processed successfully ✅"
    }
from fastapi import HTTPException
from app.utils.helpers import generate_ai_match_recommendations

@router.post("/match")
def match_internship(user: UserProfile):
    """Uses AI to find best internship matches and learning roadmap."""
    ai_response = generate_ai_match_recommendations(user.branch, user.skills)

    if "error" in ai_response:
        raise HTTPException(status_code=500, detail=f"AI Error: {ai_response['error']}")

    return {
        "name": user.name,
        "branch": user.branch,
        "email": user.email,
        "ai_suggestions": ai_response["ai_output"]
    }
