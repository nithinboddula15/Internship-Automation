import smtplib
from email.message import EmailMessage
from datetime import datetime

from config_local import sender_email, receiver_email, app_password
from logger import logger


# ──────────────────────────────────────────────
# HTML Helpers
# ──────────────────────────────────────────────

def _skill_badges(skills, color, bg):
    if not skills:
        return '<span style="color:#9ca3af;font-style:italic;">None</span>'
    return "".join(
        f'<span style="display:inline-block;background:{bg};color:{color};'
        f'font-size:12px;font-weight:600;padding:4px 10px;border-radius:20px;'
        f'margin:3px 3px 3px 0;">{skill}</span>'
        for skill in skills
    )


def _score_color(score):
    if score >= 80:
        return "#16a34a", "#dcfce7"   # green
    elif score >= 60:
        return "#d97706", "#fef9c3"   # amber
    else:
        return "#dc2626", "#fee2e2"   # red


def _build_card(internship):
    score        = internship.get("match_score", 0)
    title        = internship.get("title", "N/A")
    company      = internship.get("company", "N/A")
    location     = internship.get("location", "N/A")
    stipend      = internship.get("stipend", "N/A")
    duration     = internship.get("duration", "N/A")
    status       = internship.get("recommendation_status", "N/A")
    link         = internship.get("link", "#")
    matched      = internship.get("matched_skills", [])
    missing      = internship.get("missing_skills", [])

    txt_color, bg_color = _score_color(score)

    matched_html = _skill_badges(matched, "#166534", "#dcfce7")
    missing_html = _skill_badges(missing, "#9a3412", "#ffedd5")

    return f"""
    <!-- Internship Card -->
    <table width="100%" cellpadding="0" cellspacing="0" border="0"
           style="border:1px solid #e5e7eb;border-radius:14px;margin-bottom:24px;
                  background:#ffffff;overflow:hidden;">
      <tr>
        <!-- Left accent bar -->
        <td width="6" style="background:linear-gradient(180deg,#6366f1,#3b82f6);
                             border-radius:14px 0 0 14px;">&nbsp;</td>
        <td style="padding:24px 28px;">

          <!-- Title + Badge Row -->
          <table width="100%" cellpadding="0" cellspacing="0" border="0">
            <tr>
              <td>
                <h2 style="margin:0 0 4px 0;font-size:20px;font-weight:700;
                           color:#1e293b;line-height:1.3;">{title}</h2>
                <p style="margin:0;font-size:15px;color:#64748b;font-weight:500;">
                  🏢&nbsp;{company}
                </p>
              </td>
              <td align="right" valign="top" style="white-space:nowrap;">
                <span style="display:inline-block;background:{bg_color};color:{txt_color};
                             font-size:13px;font-weight:700;padding:6px 14px;
                             border-radius:20px;border:1.5px solid {txt_color};">
                  ⭐ {score}%
                </span>
              </td>
            </tr>
          </table>

          <!-- Status pill -->
          <p style="margin:12px 0 0 0;">
            <span style="display:inline-block;background:#ede9fe;color:#6d28d9;
                         font-size:12px;font-weight:600;padding:4px 12px;
                         border-radius:20px;">
              🏅&nbsp;{status}
            </span>
          </p>

          <!-- Divider -->
          <hr style="border:none;border-top:1px solid #f1f5f9;margin:18px 0;">

          <!-- Details grid (table-based for email clients) -->
          <table width="100%" cellpadding="0" cellspacing="0" border="0"
                 style="background:#f8fafc;border-radius:10px;padding:0;">
            <tr>
              <td style="padding:12px 16px;font-size:14px;color:#374151;
                         width:50%;vertical-align:top;">
                📍&nbsp;<strong>Location</strong><br>
                <span style="color:#6b7280;">{location}</span>
              </td>
              <td style="padding:12px 16px;font-size:14px;color:#374151;
                         width:50%;vertical-align:top;">
                💰&nbsp;<strong>Stipend</strong><br>
                <span style="color:#6b7280;">{stipend}</span>
              </td>
            </tr>
            <tr>
              <td colspan="2" style="padding:0 16px 12px 16px;font-size:14px;
                                     color:#374151;">
                ⏳&nbsp;<strong>Duration:&nbsp;</strong>
                <span style="color:#6b7280;">{duration}</span>
              </td>
            </tr>
          </table>

          <!-- Skills You Have -->
          <p style="margin:18px 0 6px 0;font-size:13px;font-weight:700;
                    color:#166534;text-transform:uppercase;letter-spacing:0.5px;">
            ✅ Skills You Have
          </p>
          <p style="margin:0;">{matched_html}</p>

          <!-- Skills To Learn -->
          <p style="margin:14px 0 6px 0;font-size:13px;font-weight:700;
                    color:#9a3412;text-transform:uppercase;letter-spacing:0.5px;">
            📚 Skills To Learn
          </p>
          <p style="margin:0;">{missing_html}</p>

          <!-- Apply Button -->
          <p style="margin:22px 0 0 0;">
            <a href="{link}"
               style="display:inline-block;background:linear-gradient(135deg,#6366f1,#3b82f6);
                      color:#ffffff;font-size:14px;font-weight:700;text-decoration:none;
                      padding:12px 28px;border-radius:8px;letter-spacing:0.3px;">
              🚀&nbsp;Apply on Internshala →
            </a>
          </p>

        </td>
      </tr>
    </table>
    """


# ──────────────────────────────────────────────
# Main HTML Email Builder
# ──────────────────────────────────────────────

def build_html_email(internships):
    today = datetime.now().strftime("%d %B %Y")
    count = len(internships)

    cards_html = "\n".join(_build_card(i) for i in internships)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Internship Report</title>
</head>
<body style="margin:0;padding:0;background:#f1f5f9;
             font-family:'Segoe UI',Arial,Helvetica,sans-serif;">

  <!-- Outer wrapper -->
  <table width="100%" cellpadding="0" cellspacing="0" border="0"
         style="background:#f1f5f9;padding:32px 16px;">
    <tr>
      <td align="center">

        <!-- Container -->
        <table width="100%" cellpadding="0" cellspacing="0" border="0"
               style="max-width:680px;background:#ffffff;border-radius:20px;
                      overflow:hidden;box-shadow:0 4px 32px rgba(0,0,0,0.08);">

          <!-- ── Header ── -->
          <tr>
            <td style="background:linear-gradient(135deg,#4f46e5 0%,#2563eb 50%,#0ea5e9 100%);
                       padding:40px 36px 32px 36px;text-align:center;">
              <p style="margin:0 0 8px 0;font-size:36px;">🚀</p>
              <h1 style="margin:0;font-size:28px;font-weight:800;color:#ffffff;
                         letter-spacing:-0.5px;line-height:1.2;">
                Internship Automation Report
              </h1>
              <p style="margin:10px 0 0 0;font-size:14px;color:#bfdbfe;">
                📅&nbsp;{today}
              </p>
            </td>
          </tr>

          <!-- ── Summary Banner ── -->
          <tr>
            <td style="background:#eff6ff;padding:20px 36px;text-align:center;
                       border-bottom:1px solid #e0eaff;">
              <p style="margin:0;font-size:15px;color:#1e40af;">
                Found&nbsp;
                <strong style="font-size:22px;color:#1d4ed8;">{count}</strong>
                &nbsp;high-match internship{"s" if count != 1 else ""} for you today
              </p>
            </td>
          </tr>

          <!-- ── Cards ── -->
          <tr>
            <td style="padding:28px 32px;">
              {cards_html}
            </td>
          </tr>

          <!-- ── Footer ── -->
          <tr>
            <td style="background:#f8fafc;border-top:1px solid #e5e7eb;
                       padding:24px 36px;text-align:center;">
              <p style="margin:0 0 4px 0;font-size:13px;color:#94a3b8;">
                🎯 Generated automatically by <strong>Internship Automation</strong>
              </p>
              <p style="margin:0;font-size:12px;color:#cbd5e1;">
                Happy Applying! Keep pushing forward 💪
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>

</body>
</html>"""


# ──────────────────────────────────────────────
# Plain-text Fallback
# ──────────────────────────────────────────────

def build_email_body(internships):
    today = datetime.now().strftime("%d %B %Y")

    lines = [
        "=" * 48,
        "  INTERNSHIP AUTOMATION REPORT",
        f"  Date : {today}",
        f"  Internships Found : {len(internships)}",
        "=" * 48,
    ]

    for idx, i in enumerate(internships, 1):
        matched = ", ".join(i.get("matched_skills", [])) or "None"
        missing = ", ".join(i.get("missing_skills", [])) or "None"
        lines += [
            "",
            f"[{idx}] {i.get('title', 'N/A').upper()}",
            f"    Company   : {i.get('company', 'N/A')}",
            f"    Location  : {i.get('location', 'N/A')}",
            f"    Stipend   : {i.get('stipend', 'N/A')}",
            f"    Duration  : {i.get('duration', 'N/A')}",
            f"    Score     : {i.get('match_score', 0)}%",
            f"    Status    : {i.get('recommendation_status', 'N/A')}",
            f"    Have      : {matched}",
            f"    Learn     : {missing}",
            f"    Apply     : {i.get('link', '#')}",
            "-" * 48,
        ]

    lines += ["", "Generated by Internship Automation 🚀", "=" * 48]
    return "\n".join(lines)


# ──────────────────────────────────────────────
# Send Email
# ──────────────────────────────────────────────

def send_email(internships):
    if not internships:
        logger.info("No internships to email.")
        return

    try:
        message = EmailMessage()
        message["Subject"] = (
            f"🚀 Internship Report | {len(internships)} High-Match Internships | "
            f"{datetime.now().strftime('%d %b %Y')}"
        )
        message["From"] = sender_email
        message["To"]   = receiver_email

        # Plain-text fallback
        message.set_content(build_email_body(internships))

        # Rich HTML version
        message.add_alternative(build_html_email(internships), subtype="html")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(message)

        logger.info("Email sent successfully!")

    except Exception as e:
        logger.error(f"Email could not be sent: {e}")