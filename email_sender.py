import smtplib
from email.message import EmailMessage

from config_local import sender_email, receiver_email, app_password


def send_email(new_internships):

    if len(new_internships) == 0:
        print("No new internships. Email not sent.")
        return

    message = EmailMessage()

    message["Subject"] = f"{len(new_internships)} New Internships Found"

    message["From"] = sender_email
    message["To"] = receiver_email

    body = "New internships found:\n\n"

    for internship in new_internships:

        body += f"""
Title: {internship['title']}
Company: {internship['company']}
Location: {internship['location']}
Stipend: {internship['stipend']}
Duration: {internship['duration']}
Link: {internship['link']}

----------------------------------------
"""

    message.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

        smtp.login(sender_email, app_password)

        smtp.send_message(message)

    print("Email Sent Successfully!")