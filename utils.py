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

    try:

        if posted_time == "today":
            return 0

        if "just now" in posted_time:
            return 0

        if "minute" in posted_time:
            return 0

        if "hour" in posted_time:
            return 0

        if "yesterday" in posted_time:
            return 1

        if "day" in posted_time:
            return int(posted_time.split()[0])

        if "week" in posted_time:
            return int(posted_time.split()[0]) * 7

        if "month" in posted_time:
            return int(posted_time.split()[0]) * 30

        if "year" in posted_time:
            return int(posted_time.split()[0]) * 365

    except (ValueError, IndexError) as e:

        logger.warning(
            f"convert_to_days: could not parse '{posted_time}': {e}. "
            "Returning 999."
        )
        return 999

    logger.warning(
        f"convert_to_days: unrecognised format '{posted_time}'. Returning 999."
    )
    return 999