import re

from logger import logger


def load_skill_database(file_path="skills.txt"):

    try:

        with open(file_path, "r", encoding="utf-8") as f:
            skills = [
                skill.strip().lower()
                for skill in f.readlines()
                if skill.strip()
            ]

        logger.info(f"Skill database loaded: {len(skills)} skills from '{file_path}'.")
        return skills

    except FileNotFoundError:

        logger.error(f"Skills file not found: '{file_path}'. Returning empty list.")
        return []

    except Exception as e:

        logger.error(f"Error loading skill database: {e}. Returning empty list.")
        return []


def extract_skills(text, skill_database):

    if not text:
        logger.warning("extract_skills: received empty text. Returning no skills.")
        return []

    text = text.lower()
    found_skills = []

    for skill in skill_database:

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text):
            found_skills.append(skill)

    result = sorted(set(found_skills))

    logger.info(f"Skills extracted from resume: {result}")
    return result