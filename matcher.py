from google import genai
from google.genai.errors import ClientError
from config_local import gemini_api_key
import json
from logger import logger

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
            model="gemini-flash-lite-latest",
            contents=prompt
        )

        return json.loads(response.text)

    except json.JSONDecodeError:

        logger.error("Gemini returned invalid JSON.")

        return {
            "match_score": 0,
            "recommendation_status": "Parse Error",
            "matched_skills": [],
            "missing_skills": [],
            "ai_reason": ["Gemini returned invalid JSON."],
            "application_advice": ""
        }

    except ClientError as e:

        logger.error(f"Gemini API quota exceeded or unavailable: {e}")

        return {
            "match_score": 0,
            "recommendation_status": "API Error",
            "matched_skills": [],
            "missing_skills": [],
            "ai_reason": ["Gemini API quota exceeded or unavailable."],
            "application_advice": ""
        }

    except Exception as e:

        logger.error(f"Unexpected Error: {e}")

        return {
            "match_score": 0,
            "recommendation_status": "Unknown Error",
            "matched_skills": [],
            "missing_skills": [],
            "ai_reason": [str(e)],
            "application_advice": ""
        }


def get_ai_skill_weights(resume_skills, internship_skills):

    if not internship_skills:
        return {}

    prompt = f"""You are a technical recruiter evaluating skill importance.

Given the candidate's resume skills and the internship's required skills,
assign an importance weight (1 to 10) to EACH internship skill,
where 10 = absolutely critical and 1 = barely relevant.

Candidate Resume Skills:
{", ".join(resume_skills)}

Internship Required Skills:
{", ".join(internship_skills)}

Return ONLY valid JSON. No markdown. No explanation.

Return exactly this format (one entry per internship skill):

{{
    "skill_name_1": 8,
    "skill_name_2": 5,
    "skill_name_3": 3
}}
"""

    try:

        response = client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=prompt
        )

        weights = json.loads(response.text)

        # Normalise: lower-case keys, clamp values 1-10
        return {
            k.lower(): max(1, min(10, int(v)))
            for k, v in weights.items()
        }

    except Exception as e:

        logger.error(f"Skill weight AI call failed: {e}. Using default weight 1.")

        return {skill.lower(): 1 for skill in internship_skills}


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

        if score >= 90:
            status = "Excellent Match"
        elif score >= 75:
            status = "Strong Match"
        elif score >= 60:
            status = "Good Match"
        elif score >= 40:
            status = "Average Match"
        else:
            status = "Weak Match"

        return {
            "match_score": score,
            "recommendation_status": status,
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