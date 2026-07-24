from excel_manager import load_existing_data
from excel_manager import save_new_data

from scraper import scrape_internships

from email_sender import send_email


old_df, existing_ids = load_existing_data()

new_internships = scrape_internships(existing_ids)

df, final_df = save_new_data(old_df, new_internships)

print("Old rows:", len(old_df))
print("New rows:", len(df))
print("Final rows:", len(final_df))

send_email(new_internships)