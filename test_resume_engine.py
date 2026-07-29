from resume_engine import (
    load_resume_skills,
    match_resume_to_internship
)

# Change this path if your resume name is different
resume_path = "resume/Nithin Boddula _ ML_Resume.pdf"

resume_skills = load_resume_skills(resume_path)

print("Resume Skills:")
print(resume_skills)

description = """
We are looking for a Machine Learning Intern.

Requirements:

Python
Pandas
NumPy
Scikit-learn
TensorFlow
Git
Docker
AWS

Knowledge of Deep Learning is preferred.
"""

result = match_resume_to_internship(
    resume_skills,
    description
)

print("\nInternship Skills:")
print(result["internship_skills"])

print("\nMatch Score:")
print(result["score"])

print("\nMatched Skills:")
print(result["matched"])

print("\nMissing Skills:")
print(result["missing"])