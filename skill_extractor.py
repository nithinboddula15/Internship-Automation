def load_skill_database(file_path="skills.txt"):

    with open(file_path, "r", encoding="utf-8") as file:

        skills = [
            skill.strip().lower()
            for skill in file.readlines()
            if skill.strip()
        ]

    return skills


import re


def extract_skills(text, skill_database):

    text = text.lower()

    found_skills = []

    for skill in skill_database:

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text):

            found_skills.append(skill)

    return sorted(list(set(found_skills)))
    