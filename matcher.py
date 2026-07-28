def calculate_match_score(resume_skills, internship_skills):

    # Convert everything to lowercase
    resume_skills = [skill.lower() for skill in resume_skills]
    internship_skills = [skill.lower() for skill in internship_skills]

    # Find matching skills
    matched_skills = []

    for skill in resume_skills:

        if skill in internship_skills:
            matched_skills.append(skill)

    # Find missing skills
    missing_skills = []

    for skill in internship_skills:

        if skill not in resume_skills:
            missing_skills.append(skill)

    # Calculate percentage
    if len(internship_skills) == 0:
        score = 0
    else:
        score = round((len(matched_skills) / len(internship_skills)) * 100)

    return score, matched_skills, missing_skills