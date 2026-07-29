from skill_extractor import load_skill_database, extract_skills

skills_db = load_skill_database()

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

found_skills = extract_skills(description, skills_db)

print(found_skills)