import json
import os

from logger import logger

CACHE_FILE = "data/title_cache.json"


def load_title_cache():
    """
    Load cached title classifications.
    """

    if not os.path.exists(CACHE_FILE):

        logger.info("Title cache not found. Creating new cache.")
        return {}

    try:

        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)

        with open(CACHE_FILE, "r", encoding="utf-8") as f:        

            cache = json.load(f)

        logger.info(f"Title cache loaded: {len(cache)} entries.")

        return cache

    except json.JSONDecodeError:
        logger.error("Title cache is corrupted. Starting fresh.")
        return {}

    except Exception as e:
        logger.error(f"Failed to load title cache: {e}")
        return {}   


def get_cached_title(cache, title):
    """
    Return cached title classification if available.
    """

    key = title.lower().strip()

    return cache.get(key)


def cache_title(cache, title, result):
    """
    Store title classification in memory.
    """

    key = title.lower().strip()

    cache[key] = result


def save_title_cache(cache):
    """
    Save title cache to disk.
    """

    try:

        with open(CACHE_FILE, "w", encoding="utf-8") as f:

            json.dump(
                cache,
                f,
                indent=4,
                ensure_ascii=False
            )

        logger.info(
            f"Title cache saved: {len(cache)} entries."
        )

    except Exception as e:

        logger.error(f"Failed to save title cache: {e}")