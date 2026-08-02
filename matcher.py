from google import genai
from google.genai.errors import ClientError
from config_local import gemini_api_key
from recommendation import generate_recommendation
import json

client = genai.Client(api_key=gemini_api_key)


def keyword_match(resume_skills, internship_skills):

    resume_skills = [skill.lower() for skill in resume_skills]
    internship_skills = [skill.lower() for skill in internship_skills]

    matched_skills = []

    for skill in resume_skills:
        if skill in internship_skills:
            matched_skills.append(skill)

    missing_skills = []

    for skill in internship_skills:
        if skill not in resume_skills:
            missing_skills.append(skill)

    if len(internship_skills) == 0:
        score = 0
    else:
        score = round(
            (len(matched_skills) / len(internship_skills)) * 100
        )

    return score, matched_skills, missing_skills


def call_gemini_api(client, prompt):

    try:

        response = client.models.generate_content(
            model="models/gemini-3.5-flash",
            contents=prompt
        )

        return json.loads(response.text)

    except json.JSONDecodeError:

        print("Gemini returned invalid JSON.")

        return {
            "match_score": 0,
            "recommendation_status": "Parse Error",
            "matched_skills": [],
            "missing_skills": [],
            "ai_reason": ["Gemini returned invalid JSON."],
            "application_advice": ""
        }

    except ClientError as e:

        print(f"Gemini API quota exceeded or unavailable: {e}")

        return {
            "match_score": 0,
            "recommendation_status": "API Error",
            "matched_skills": [],
            "missing_skills": [],
            "ai_reason": ["Gemini API quota exceeded or unavailable."],
            "application_advice": ""
        }

    except Exception as e:

        print(f"Unexpected Error: {e}")

        return {
            "match_score": 0,
            "recommendation_status": "Unknown Error",
            "matched_skills": [],
            "missing_skills": [],
            "ai_reason": [str(e)],
            "application_advice": ""
        }


def semantic_match(resume_text, internship):

    prompt = f"""
You are an expert technical recruiter.

Evaluate how well the candidate matches this internship.

Resume:

{resume_text}

----------------------------------------------------

Internship Title:
{internship["title"]}

Company:
{internship["company"]}

Description:
{internship["description"]}

Return ONLY valid JSON.

Do NOT use markdown.
Do NOT wrap the JSON in ```json.

Return exactly this format:

{{
    "match_score": 0,
    "recommendation_status": "",
    "matched_skills": [],
    "missing_skills": [],
    "ai_reason": [],
    "application_advice": ""
}}
"""

    return call_gemini_api(client, prompt)


def match_resume_to_internship(
    resume_skills,
    internship_skills,
    resume_text=None,
    internship=None
):

    # ---------- Fast keyword matching ----------
    score, matched, missing = keyword_match(
        resume_skills,
        internship_skills
    )

    # If no resume text or internship object,
    # return keyword result only.

    if resume_text is None or internship is None:

        return {
            "match_score": score,
            "recommendation_status": generate_recommendation(score)["status"],
            "matched_skills": matched,
            "missing_skills": missing,
            "ai_reason": [],
            "application_advice": "",
            "internship_skills": internship_skills
        }

    # ---------- AI Semantic Matching ----------

    ai_result = semantic_match(
        resume_text,
        internship
    )

    ai_result["internship_skills"] = internship_skills

    return ai_result