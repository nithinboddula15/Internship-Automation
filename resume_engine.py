from resume_parser import extract_resume_text
from skill_extractor import load_skill_database, extract_skills
from resume_matcher import calculate_match_score



# Load once
skill_database = load_skill_database()


def load_resume_skills(resume_path):

    resume_text = extract_resume_text(resume_path)

    resume_skills = extract_skills(
        resume_text,
        skill_database
    )

    return resume_skills


def match_resume_to_internship(resume_skills, internship_description):

    internship_skills = extract_skills(
        internship_description,
        skill_database
    )
    print("\n==============================")
    print("Resume Skills:", resume_skills)
    print("Internship Skills:", internship_skills)
    print("==============================")
    score, matched, missing = calculate_match_score(
        resume_skills,
        internship_skills
    )

    return {
        "score": score,
        "matched": matched,
        "missing": missing,
        "internship_skills": internship_skills
    }