from logger import logger


def convert_to_days(posted_time):
    """
    Convert a human-readable 'posted time' string into an integer number of days.
    Returns 999 if the format is unrecognised.
    """

    if not posted_time:
        logger.warning("convert_to_days: received empty posted_time. Returning 999.")
        return 999

    posted_time = posted_time.lower().strip()

    # Posted today
    if any(word in posted_time for word in ["today", "just now", "minute", "hour"]):
        return 0

    # Posted yesterday
    if "yesterday" in posted_time:
        return 1

    multipliers = {
        "day": 1,
        "week": 7,
        "month": 30,
        "year": 365
    }

    try:

        for unit, multiplier in multipliers.items():

            if unit in posted_time:
                return int(posted_time.split()[0]) * multiplier

    except (ValueError, IndexError) as e:

        logger.warning(
            f"convert_to_days: could not parse '{posted_time}': {e}. Returning 999."
        )

        return 999

    logger.warning(
        f"convert_to_days: unrecognised format '{posted_time}'. Returning 999."
    )

    return 999