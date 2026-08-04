import json
import time
from google import genai
from google.genai.errors import ClientError
from config_local import gemini_api_key
from logger import logger

client = genai.Client(api_key=gemini_api_key)


def keyword_match(resume_skills, internship_skills):

    resume = {
        skill.lower().strip()
        for skill in resume_skills
    }

    internship = {
        skill.lower().strip()
        for skill in internship_skills
    }

    matched = sorted(resume & internship)
    missing = sorted(internship - resume)

    if not internship:
        score = 0
    else:
        score = round(len(matched) / len(internship) * 100)

    return score, matched, missing



from google.genai.errors import ClientError


def call_gemini_api(client, prompt):

    for attempt in range(2):   # First try + one retry

        try:

            response = client.models.generate_content(
                model="gemini-flash-lite-latest",
                contents=prompt
            )

            text = response.text.strip()

            # Remove markdown if Gemini returns it
            if text.startswith("```json"):
                text = text.replace("```json", "").replace("```", "").strip()

            elif text.startswith("```"):
                text = text.replace("```", "").strip()

            return json.loads(text)

        except json.JSONDecodeError:

            logger.warning("Gemini returned invalid JSON.")

            if attempt == 0:
                logger.info("Retrying in 2 seconds...")
                time.sleep(2)
                continue

            return {
                "match_score": 0,
                "recommendation_status": "Parse Error",
                "matched_skills": [],
                "missing_skills": [],
                "strengths": [],
                "weaknesses": [],
                "ai_reason": [
                    "Gemini returned invalid JSON after retry."
                ],
                "application_advice": ""
            }

        except ClientError as e:

            logger.warning(f"Gemini API Error: {e}")

            if attempt == 0:
                logger.info("Retrying in 5 seconds...")
                time.sleep(5)
                continue

            return {
                "match_score": 0,
                "recommendation_status": "API Error",
                "matched_skills": [],
                "missing_skills": [],
                "strengths": [],
                "weaknesses": [],
                "ai_reason": [
                    "Gemini API unavailable after retry."
                ],
                "application_advice": ""
            }

        except Exception as e:

            logger.error(f"Unexpected Error: {e}")

            return {
                "match_score": 0,
                "recommendation_status": "Unknown Error",
                "matched_skills": [],
                "missing_skills": [],
                "strengths": [],
                "weaknesses": [],
                "ai_reason": [str(e)],
                "application_advice": ""
            }



def semantic_match(
    resume_text,
    resume_skills,
    internship
):
    prompt = f"""
You are a Senior Technical Recruiter with expertise in hiring interns for AI, Machine Learning, Data Science, and Software Engineering roles.

Your task is to evaluate how well the candidate matches this internship.

Evaluate using ALL of the following:

1. Resume skills
2. Resume projects and practical experience
3. Internship required skills
4. Internship description
5. Overall career relevance

Scoring Rules:

90-100 : Excellent Match
75-89  : Strong Match
60-74  : Good Match
40-59  : Average Match
0-39   : Weak Match

Resume:

{resume_text}
Resume Skills:

{", ".join(internship["resume_skills"])}

------------------------------------------------------------

Internship Title:
{internship["title"]}

Company:
{internship["company"]}

Internship Description:
{internship["description"]}

------------------------------------------------------------

Return ONLY valid JSON.

Do NOT return markdown.
Do NOT return explanations outside JSON.

Return exactly this format:

{{
    "match_score": 0,
    "recommendation_status": "",
    "matched_skills": [],
    "missing_skills": [],
    "strengths": [],
    "weaknesses": [],
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
        resume_skills,
        internship
    )

    # Python is the source of truth
    ai_result["matched_skills"] = matched
    ai_result["missing_skills"] = missing
    ai_result["internship_skills"] = internship_skills

    return ai_result