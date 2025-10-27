# app/routes/resume_generate_routes.py
from fastapi import APIRouter, Body, HTTPException
from openai import OpenAI
from fpdf import FPDF
import os
import re
import textwrap
from app.utils.payment_helper import verify_payment

router = APIRouter(prefix="/api/resume", tags=["Resume Generator"])

# Initialize OpenAI client (ensure OPENAI_API_KEY is set in your env)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Helper: sanitize filename
def _safe_filename(name: str) -> str:
    name = (name or "candidate").strip()
    # keep letters, numbers, dash and underscore
    safe = re.sub(r"[^\w\-]", "_", name)
    return safe[:120]  # limit length

# helper to break extremely long tokens by inserting soft breaks
def _break_long_tokens(text: str, max_token_len: int = 60) -> str:
    parts = []
    for token in text.split(" "):
        if len(token) > max_token_len:
            chunks = [token[i:i + max_token_len] for i in range(0, len(token), max_token_len)]
            parts.append(" ".join(chunks))
        else:
            parts.append(token)
    return " ".join(parts)

@router.post("/generate")
async def generate_resume(data: dict = Body(...)):
    """
    Generates AI-based resume (Paid Feature).
    Expected body shape:
    {
        "payment": { "order_id": "...", "payment_id": "...", "signature": "..." },
        "name": "Amit Sharma",
        "education": "...",
        "skills": ["Python", "IoT"],
        "projects": [...],
        "experience": "...",
        "email": "..."
    }
    """
    try:
        # --- Payment verification (skip if SKIP_PAYMENT_CHECK=true for local dev) ---
        skip_check = os.getenv("SKIP_PAYMENT_CHECK", "false").lower() in ("1", "true", "yes")
        if not skip_check:
            payment_data = data.get("payment")
            if not payment_data:
                raise HTTPException(
                    status_code=402,
                    detail="Payment required. Provide payment object with order_id, payment_id and signature."
                )
            verified = verify_payment(
                payment_data.get("order_id"),
                payment_data.get("payment_id"),
                payment_data.get("signature")
            )
            if not verified:
                raise HTTPException(
                    status_code=403,
                    detail="Payment verification failed or missing. Please complete payment."
                )
        # --- End payment verification ---

        name = data.get("name") or "Candidate"
        safe_name = _safe_filename(name)
        # build prompt from provided data (keep it concise)
        prompt = f"""
Create a clean, ATS-friendly, professional resume for {name}.
Use the following details (if provided) and produce sections:
- Professional Summary
- Education
- Skills
- Projects
- Experience
- Contact Information

User data:
{{
  "education": {data.get("education")},
  "skills": {data.get("skills")},
  "projects": {data.get("projects")},
  "experience": {data.get("experience")},
  "email": {data.get("email")}
}}
Please output plain text suitable for a one-page resume.
"""
        # Call OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert resume writer. Generate clear, concise, ATS-friendly resumes."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1200
        )

        # Extract AI content safely
        try:
            ai_resume = response.choices[0].message.content.strip()
        except Exception:
            # fallback in case of unexpected response shape
            ai_resume = str(response)

        # Ensure output folder
        os.makedirs("temp_uploads", exist_ok=True)
        filename = f"{safe_name}_AI_Resume.pdf"
        pdf_path = os.path.join("temp_uploads", filename)

        # --- SAFE PDF CREATION (handles very long tokens) ---
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=12)

        # choose a conservative font size
        font_size = 11
        pdf.set_font("Arial", size=font_size)

        try:
            for paragraph in ai_resume.split("\n\n"):
                paragraph = paragraph.strip()
                if not paragraph:
                    continue

                # First pre-process to break huge tokens
                safe_par = _break_long_tokens(paragraph, max_token_len=60)

                # Wrap the paragraph to approx 90 characters per line (safe)
                wrapped_lines = textwrap.wrap(safe_par, width=90, break_long_words=True, replace_whitespace=True)

                for line in wrapped_lines:
                    if line.strip() == "":
                        continue
                    pdf.multi_cell(0, 7, line)
                pdf.ln(2)

            pdf.output(pdf_path)
        except Exception as pdf_err:
            # fallback: write a very simple, safe, plain text PDF by writing line-by-line
            try:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=10)
                safe_text = _break_long_tokens(ai_resume, max_token_len=40)
                for i in range(0, len(safe_text), 70):
                    pdf.cell(0, 6, safe_text[i:i + 70], ln=True)
                pdf.output(pdf_path)
            except Exception as fallback_err:
                raise HTTPException(status_code=500, detail=f"PDF generation failed: {pdf_err} | fallback failed: {fallback_err}")

        preview = ai_resume[:2000]  # return a preview (trim if very long)
        download_url = f"/download/{filename}"

        return {
            "status": "success",
            "message": "AI Resume generated successfully ✅",
            "download_url": download_url,
            "preview": preview
        }

    except HTTPException:
        # re-raise HTTPExceptions untouched
        raise
    except Exception as e:
        # catch-all for unexpected errors
        raise HTTPException(status_code=500, detail=f"Server error while generating resume: {str(e)}")
