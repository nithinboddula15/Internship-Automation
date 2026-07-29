from career_profile import SKILL_WEIGHTS


def calculate_match_score(resume_skills, internship_skills):

    resume_set = set(skill.lower() for skill in resume_skills)
    internship_set = set(skill.lower() for skill in internship_skills)

    matched = []
    missing = []

    earned_weight = 0
    total_weight = 0

    for skill in internship_set:

        weight = SKILL_WEIGHTS.get(skill, 1)

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
    print("Matched:", matched)
    print("Missing:", missing)
    print("Total Weight:", total_weight)
    print("Earned Weight:", earned_weight)
    print("Score:", score)

    return score, sorted(matched), sorted(missing)