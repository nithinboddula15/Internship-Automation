def convert_to_days(posted_time):

    posted_time = posted_time.lower().strip()

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

    return 999