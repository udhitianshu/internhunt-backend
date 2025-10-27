from fastapi import APIRouter, UploadFile, File, HTTPException
from openai import OpenAI
import os
from app.utils.resume_helper import extract_text_from_resume

router = APIRouter(prefix="/api/resume", tags=["Resume Review"])

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@router.post("/review")
async def review_resume(file: UploadFile = File(...)):
    """
    Reviews the uploaded resume and provides grammar, clarity, and formatting suggestions.
    """
    try:
        os.makedirs("temp_uploads", exist_ok=True)
        file_path = f"temp_uploads/{file.filename}"
        with open(file_path, "wb") as f:
            f.write(await file.read())

        resume_text = extract_text_from_resume(file_path)

        prompt = f"""
        You are an expert HR recruiter.
        Review this resume and provide detailed feedback on:
        - Clarity and structure
        - Grammar and tone
        - ATS keyword optimization
        - Professional impression
        Return in structured JSON format:
        {{
            "summary": "...",
            "suggestions": ["...", "..."]
        }}
        Resume text:
        {resume_text}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are a resume review assistant."},
                      {"role": "user", "content": prompt}]
        )

        feedback = response.choices[0].message.content.strip()
        os.remove(file_path)

        return {"review": feedback}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
