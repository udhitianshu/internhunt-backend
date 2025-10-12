from fastapi import APIRouter, UploadFile, File, HTTPException
import os
from app.utils.resume_helper import extract_text_from_resume, analyze_resume_with_ai

router = APIRouter(prefix="/api/resume", tags=["Resume Analyzer"])

@router.post("/analyze")
async def analyze_resume(file: UploadFile = File(...)):
    """Analyze uploaded resume using AI feedback."""
    try:
        # Save uploaded file temporarily
        file_path = f"temp_uploads/{file.filename}"
        os.makedirs("temp_uploads", exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Extract and analyze
        resume_text = extract_text_from_resume(file_path)
        ai_feedback = analyze_resume_with_ai(resume_text)

        # Clean up
        os.remove(file_path)
        return ai_feedback

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
