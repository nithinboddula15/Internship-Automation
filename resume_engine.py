from resume_parser import extract_resume_text
from skill_extractor import load_skill_database, extract_skills

skill_database = load_skill_database()

def load_resume(resume_path):

    resume_text = extract_resume_text(resume_path)

    resume_skills = extract_skills(
        resume_text,
        skill_database
    )

    return resume_text, resume_skills