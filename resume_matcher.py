from logger import logger


def calculate_match_score(resume_skills, internship_skills, ai_skill_weights=None):
    """
    Calculate weighted match score using AI-generated skill weights.

    ai_skill_weights: dict of {skill_name (lower): weight (1-10)}
                      provided by Gemini. Falls back to 1 if not given.
    """

    if ai_skill_weights is None:
        ai_skill_weights = {}

    resume_set = set(skill.lower() for skill in resume_skills)
    internship_set = set(skill.lower() for skill in internship_skills)

    matched = []
    missing = []

    earned_weight = 0
    total_weight = 0

    for skill in internship_set:

        weight = ai_skill_weights.get(skill, 1)

        total_weight += weight

        if skill in resume_set:

            matched.append(skill)

            earned_weight += weight

        else:

            missing.append(skill)

    if total_weight == 0:

        score = 0

    else:

        score = round((earned_weight / total_weight) * 100)

    logger.info(f"Matched: {sorted(matched)}")
    logger.info(f"Missing: {sorted(missing)}")
    logger.info(f"Total Weight: {total_weight} | Earned: {earned_weight} | Score: {score}%")

    return score, sorted(matched), sorted(missing)