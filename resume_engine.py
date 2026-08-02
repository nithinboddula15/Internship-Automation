from resume_parser import extract_resume_text
from skill_extractor import load_skill_database, extract_skills
from resume_matcher import calculate_match_score
from matcher import semantic_match
from matcher import match_resume_to_internship  


# Load once
skill_database = load_skill_database()


def load_resume(resume_path):

    resume_text = extract_resume_text(resume_path)

    resume_skills = extract_skills(
        resume_text,
        skill_database
    )

    return resume_text, resume_skills


def match_resume_to_internship(
    resume_skills,
    internship_skills,
    resume_text=None,
    internship=None
):

    # ---------- Fast Keyword Match ----------

    score, matched, missing = calculate_match_score(
        resume_skills,
        internship_skills
    )

    # ----------- LOW SCORE -------------

    if score < 30:

        return {
            "match_score": score,
            "recommendation_status": "Keyword Filtered",
            "matched_skills": matched,
            "missing_skills": missing,
            "internship_skills": internship_skills,
            "ai_reason": [
                "Skipped AI because keyword score is below 30%."
            ],
            "application_advice":
            "Not enough matching skills. Learn the missing skills first."
        }

    # ----------- AI MATCH -------------

    ai_result = semantic_match(
        resume_text,
        internship
    )

    ai_result["internship_skills"] = internship_skills

    return ai_result