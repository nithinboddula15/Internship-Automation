from google import genai
from config_local import gemini_api_key

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


def semantic_match(resume_text, internship):

    prompt = f"""
You are an expert technical recruiter.

Evaluate how well the candidate matches this internship.

Resume:

{resume_text}

----------------------------

Internship Title:
{internship["title"]}

Company:
{internship["company"]}

Description:
{internship["description"]}

Return ONLY valid JSON.

{{
    "match_score":0,
    "recommendation_status":"",
    "matched_skills":[],
    "missing_skills":[],
    "ai_reason":[]
}}
"""

    response = client.models.generate_content(
        model="models/gemini-3.5-flash",
        contents=prompt
    )

    return response.text


def match_resume_to_internship(
    resume_skills,
    internship_skills,
    resume_text=None,
    internship=None
):

    score, matched, missing = keyword_match(
        resume_skills,
        internship_skills
    )

    return {
        "match_score": score,
        "matched_skills": matched,
        "missing_skills": missing
    }