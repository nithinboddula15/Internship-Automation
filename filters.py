from utils import convert_to_days

MAX_DAYS = 7

allowed_keywords = [
    "ai",
    "artificial intelligence",
    "machine learning",
    "ml",
    "python",
    "data science",
    "data analyst",
    "analytics",
    "computer vision",
    "deep learning",
    "nlp",
    "llm",
    "genai",
    "agent",
]


def role_matches(title):

    title = title.lower()

    return any(keyword in title for keyword in allowed_keywords)


def recent_post(posted_time):

    days = convert_to_days(posted_time)

    return days <= MAX_DAYS