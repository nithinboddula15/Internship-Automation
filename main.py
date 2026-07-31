from excel_manager import load_existing_data
from excel_manager import save_new_data

from scraper import scrape_internships

from email_sender import send_email

from resume_engine import load_resume_skills


RESUME_PATH = "resume/Nithin Boddula _ ML_Resume.pdf"


resume_skills = load_resume_skills(RESUME_PATH)


old_df, existing_ids = load_existing_data()

new_internships = scrape_internships(
    existing_ids,
    resume_skills
)

df, final_df = save_new_data(old_df, new_internships)

print("Old rows:", len(old_df))
print("New rows:", len(df))
print("Final rows:", len(final_df))

# Excellent Matches
excellent = [
    internship
    for internship in new_internships
    if internship["match_score"] >= 90
]

# Strong Matches
strong = [
    internship
    for internship in new_internships
    if 75 <= internship["match_score"] < 90
]

# Decide what to email
if excellent:
    email_list = excellent

elif strong:
    email_list = strong

else:
    email_list = sorted(
        new_internships,
        key=lambda x: x["match_score"],
        reverse=True
    )[:5]

send_email(email_list)