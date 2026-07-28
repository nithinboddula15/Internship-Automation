from matcher import calculate_match_score

resume_skills = [
    "Python",
    "Git",
    "Machine Learning",
    "Pandas"
]

internship_skills = [
    "Python",
    "SQL",
    "Git",
    "TensorFlow"
]

score, matched, missing = calculate_match_score(
    resume_skills,
    internship_skills
)

print("Match Score:", score)
print("Matched Skills:", matched)
print("Missing Skills:", missing)