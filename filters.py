from utils import convert_to_days

from career import QUICK_FILTER_KEYWORDS, MAX_POSTED_DAYS

from logger import logger


def role_matches(title):
    """Return True if the internship title contains a relevant keyword."""

    title_lower = title.lower()
    matched = any(keyword in title_lower for keyword in QUICK_FILTER_KEYWORDS)

    if not matched:
        logger.debug(f"role_matches: no keyword matched for title='{title}'")

    return matched


def recent_post(posted_time):
    """Return True if the internship was posted within MAX_POSTED_DAYS days."""

    days = convert_to_days(posted_time)
    is_recent = days <= MAX_POSTED_DAYS

    if not is_recent:
        logger.debug(
            f"recent_post: '{posted_time}' → {days} days > {MAX_POSTED_DAYS} limit."
        )

    return is_recent