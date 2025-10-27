from fastapi import APIRouter, UploadFile, File, Body, HTTPException
from app.utils.resume_helper import extract_text_from_resume
from openai import OpenAI
import requests
import os

router = APIRouter(prefix="/api/internships", tags=["Internship Finder"])
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@router.post("/find")
async def find_internships(
    skills: list[str] = Body(default=[]),
    file: UploadFile = File(default=None)
):
    """
    Matches provided skills or resume with live internships.
    Currently pulls mock or static data for demo purpose.
    """
    try:
        if file:
            os.makedirs("temp_uploads", exist_ok=True)
            file_path = f"temp_uploads/{file.filename}"
            with open(file_path, "wb") as f:
                f.write(await file.read())
            resume_text = extract_text_from_resume(file_path)
            os.remove(file_path)

            prompt = f"Extract 5 most relevant skills from this resume:\n\n{resume_text}"
            skill_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            skills = skill_response.choices[0].message.content.split(",")

        if not skills:
            raise HTTPException(status_code=400, detail="No skills provided or detected.")

        # Dummy internship dataset (replace later with API)
        internships = [
            {"title": "IoT Intern", "company": "Bosch", "platform": "Internshala", "link": "https://internshala.com/iot"},
            {"title": "ML Intern", "company": "TCS", "platform": "LinkedIn", "link": "https://linkedin.com/ml-intern"},
            {"title": "Python Developer Intern", "company": "Infosys", "platform": "Wellfound", "link": "https://wellfound.com/python-intern"}
        ]

        prompt2 = f"From this list, pick top 3 internships most relevant to these skills: {skills} \n {internships}"
        ranking = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt2}]
        )

        return {
            "skills_used": skills,
            "best_matches": ranking.choices[0].message.content
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
