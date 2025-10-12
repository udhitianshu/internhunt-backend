import pdfplumber
import docx
import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_text_from_resume(file_path: str) -> str:
    """Extract text from PDF or DOCX resume."""
    text = ""
    if file_path.endswith(".pdf"):
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    else:
        raise ValueError("Unsupported file format. Please upload PDF or DOCX.")
    return text.strip()

def analyze_resume_with_ai(resume_text: str) -> dict:
    """Send resume text to OpenAI and return clean JSON feedback."""
    prompt = f"""
    You are an expert resume reviewer.
    Analyze the following resume text and return *strictly valid JSON* with this format:

    {{
      "summary": "Short professional summary of the resume",
      "missing_sections": ["list of missing or weak sections"],
      "suggestions": ["list of concrete improvement tips"]
    }}

    Resume Text:
    {resume_text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a precise JSON-generating resume review assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    ai_reply = response.choices[0].message.content

    # Ensure the response is valid JSON
    try:
        structured_output = json.loads(ai_reply)
    except json.JSONDecodeError:
        # Try to extract JSON from messy output
        try:
            json_start = ai_reply.find("{")
            json_end = ai_reply.rfind("}") + 1
            structured_output = json.loads(ai_reply[json_start:json_end])
        except Exception:
            structured_output = {"summary": ai_reply, "missing_sections": [], "suggestions": []}

    return structured_output
