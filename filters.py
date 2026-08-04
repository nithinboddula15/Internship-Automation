from utils.utils import convert_to_days
from career import QUICK_FILTER_KEYWORDS, MAX_POSTED_DAYS, NEGATIVE_KEYWORDS
from logger import logger



def quick_filter(title):
    """
    Returns:
        True   -> definitely relevant
        False  -> definitely irrelevant
        None   -> uncertain (use AI)
    """

    title_lower = title.lower()

    # Reject obvious irrelevant roles
    for keyword in NEGATIVE_KEYWORDS:
        if keyword in title_lower:
            logger.info(f"Negative filter matched: '{title}'")
            return False

    # Accept obvious AI/ML/Data roles
    for category in QUICK_FILTER_KEYWORDS.values():
        for keyword in category:
            if keyword in title_lower:
                logger.debug(f"Quick filter matched '{keyword}'")
                return True

    # Let AI decide
    logger.info(f"Needs AI classification: '{title}'")
    return None

def recent_post(posted_time):
    """Return True if the internship was posted within MAX_POSTED_DAYS days."""

    days = convert_to_days(posted_time)

    is_recent = days <= MAX_POSTED_DAYS

    if not is_recent:
        logger.info(
            f"Old internship: {posted_time} ({days} days old)"
        )

    return is_recent

def skill_overlap(card_skills, resume_skills):
    """
    Returns True if at least one skill overlaps.
    """

    if not card_skills:
        return True

    card = {
        skill.lower().strip()
        for skill in card_skills
    }

    resume = {
        skill.lower().strip()
        for skill in resume_skills
    }

    overlap = card & resume

    if overlap:
        logger.debug(
            f"Skill overlap: {', '.join(overlap)}"
        )
        return True

    logger.info(
    f"No skill overlap. Internship: {', '.join(card_skills)}"
    )
    return False