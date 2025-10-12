import json
import os
import re
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def clean_text(text: str) -> str:
    """Cleans unwanted spaces and symbols from input."""
    return text.strip().title()


def generate_ai_match_recommendations(branch: str, skills: list[str]) -> dict:
    """Uses OpenAI to generate internship recommendations and learning roadmap."""

    prompt = f"""
    The student is from the {branch} branch and knows the following skills: {', '.join(skills)}.
    Suggest 3 best-matching internship roles based on their skills,
    list the top 3 missing skills they should learn next,
    and provide a 30-day step-by-step learning roadmap.
    Return the response strictly as valid JSON only, no markdown, no explanation text, just JSON like this:
    {{
      "internships": [],
      "missing_skills": [],
      "roadmap": []
    }}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a precise JSON generator for career guidance output. You must return valid JSON only.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )

        text = response.choices[0].message.content.strip()

        # ✅ Remove unwanted markdown formatting or code fences
        text = re.sub(r"^```(json)?|```$", "", text.strip(), flags=re.MULTILINE).strip()

        # ✅ Try parsing the cleaned JSON
        parsed_json = json.loads(text)
        return {"ai_output": parsed_json}

    except json.JSONDecodeError:
        # Fallback: return raw text for debugging
        return {
            "ai_output": {
                "raw_text": text,
                "error": "Invalid JSON returned by AI (after cleaning)"
            }
        }

    except Exception as e:
        return {"error": f"AI Error: {str(e)}"}
