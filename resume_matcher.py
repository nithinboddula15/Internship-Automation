def load_skills(file_path="skills.txt"):

    with open(file_path, "r", encoding="utf-8") as file:

        skills = [line.strip().lower() for line in file if line.strip()]

    return skills


def extract_resume_skills(resume_text):

    known_skills = load_skills()

    resume_text = resume_text.lower()

    found_skills = []

    for skill in known_skills:

        if skill in resume_text:
            found_skills.append(skill)

    return found_skills