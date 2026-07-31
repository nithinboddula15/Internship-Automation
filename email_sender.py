import smtplib
from email.message import EmailMessage
from datetime import datetime

from config_local import sender_email, receiver_email, app_password


def build_internship_card(internship):

    matched = "\n".join(
        f"✔ {skill}" for skill in internship["matched_skills"]
    ) or "None"

    missing = "\n".join(
        f"• {skill}" for skill in internship["missing_skills"]
    ) or "None"

    return f"""
══════════════════════════════════════════════

🏆 {internship['title'].upper()}

🏢 Company
{internship['company']}

📍 Location
{internship['location']}

💰 Stipend
{internship['stipend']}

⏳ Duration
{internship['duration']}

⭐ Match Score
{internship['match_score']}%

🏅 Recommendation
{internship['recommendation_status']}

──────────────────────────────────────────────

✅ Skills You Already Have

{matched}

──────────────────────────────────────────────

📚 Skills To Learn

{missing}

──────────────────────────────────────────────

🔗 Apply Here

{internship['link']}
"""


def build_email_body(internships):

    today = datetime.now().strftime("%d %B %Y")

    body = f"""
══════════════════════════════════════════════

🚀 INTERNSHIP AUTOMATION REPORT

📅 Date : {today}

📊 Summary

Internships Sent : {len(internships)}

══════════════════════════════════════════════
"""

    for internship in internships:
        body += build_internship_card(internship)

    body += """

══════════════════════════════════════════════

🎯 Generated Automatically by Internship Automation

Happy Applying 🚀

══════════════════════════════════════════════
"""

    return body


def send_email(internships):

    if len(internships) == 0:
        print("No internships to email.")
        return

    try:

        message = EmailMessage()

        message["Subject"] = (
            f"🚀 Internship Report | {len(internships)} High Match Internships"
        )

        message["From"] = sender_email
        message["To"] = receiver_email

        message.set_content(build_email_body(internships))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

            smtp.login(sender_email, app_password)

            smtp.send_message(message)

        print("Email Sent Successfully!")

    except Exception as e:
        print("Email could not be sent:", e)

