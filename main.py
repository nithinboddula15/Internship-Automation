import sys

from logger import logger
from excel_manager import load_existing_data, save_new_data
from scraper import scrape_internships
from email_sender import send_email
from resume_engine import load_resume
from config import RESUME_PATH




def main():

    logger.info("=" * 50)
    logger.info("Internship Automation Started")
    logger.info("=" * 50)

    # ---------- Load Resume ----------
    try:

        resume_text, resume_skills = load_resume(RESUME_PATH)
        logger.info(f"Resume loaded. Skills found: {len(resume_skills)}")

    except FileNotFoundError:

        logger.error(f"Resume not found at '{RESUME_PATH}'. Aborting.")
        sys.exit(1)

    except Exception as e:

        logger.error(f"Failed to load resume: {e}. Aborting.")
        sys.exit(1)

    # ---------- Load Existing Data ----------
    old_df, existing_ids = load_existing_data()

    # ---------- Scrape Internships ----------
    new_internships = scrape_internships(
        existing_ids,
        resume_text,
        resume_skills
    )

    logger.info(f"Scraping complete. {len(new_internships)} new internship(s) found.")

    # ---------- Save Data ----------
    if new_internships:

        df, final_df = save_new_data(
            old_df,
            new_internships
        )

        logger.info(f"Old rows : {len(old_df)}")
        logger.info(f"New rows : {len(df)}")
        logger.info(f"Final rows: {len(final_df)}")

    else:

        logger.info("No new internships. Excel not updated.")

    # ---------- Email Decision ----------
    if not new_internships:
        logger.info("No new internships to email.")
        return

    excellent = [i for i in new_internships if i.get("match_score", 0) >= 90]
    strong    = [i for i in new_internships if 75 <= i.get("match_score", 0) < 90]

    if excellent:
        email_list = excellent
        logger.info(f"Emailing {len(email_list)} Excellent Match(es).")

    elif strong:
        email_list = strong
        logger.info(f"Emailing {len(email_list)} Strong Match(es).")

    else:
        email_list = sorted(
            new_internships,
            key=lambda x: x.get("match_score", 0),
            reverse=True
        )[:5]
        logger.info(
            f"No excellent/strong matches. Emailing top {len(email_list)} by score."
        )

    try:

        send_email(email_list)

    except Exception as e:

        logger.error(
            f"Email sending failed: {e}"
        )       

    logger.info("=" * 50)
    logger.info("Internship Automation Finished")
    logger.info("=" * 50)


if __name__ == "__main__":
    main()