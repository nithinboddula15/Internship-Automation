from utils import convert_to_days
from career import QUICK_FILTER_KEYWORDS, MAX_POSTED_DAYS
from logger import logger




def quick_filter(title):
    """
    Return True if the internship title contains
    any relevant keyword.
    """

    title_lower = title.lower()

    for keyword in QUICK_FILTER_KEYWORDS:

        if keyword in title_lower:
            logger.debug(
                f"Quick filter matched '{keyword}' in '{title}'"
            )
            return True

    logger.info(f"Quick filter failed: '{title}'")
    return False


def recent_post(posted_time):
    """Return True if the internship was posted within MAX_POSTED_DAYS days."""

    days = convert_to_days(posted_time)

    is_recent = days <= MAX_POSTED_DAYS

    if not is_recent:
        logger.info(
            f"Old internship: {posted_time} ({days} days old)"
        )

    return is_recent