import json
import os

from logger import logger

CACHE_FILE = "data/ai_cache.json"


def load_cache():

    if not os.path.exists(CACHE_FILE):
        logger.info(f"Cache file not found at '{CACHE_FILE}'. Starting fresh.")
        return {}

    try:

        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            cache = json.load(f)

        logger.info(f"Cache loaded: {len(cache)} entries from '{CACHE_FILE}'.")
        return cache

    except json.JSONDecodeError as e:

        logger.error(
            f"Cache file '{CACHE_FILE}' is corrupt (JSONDecodeError: {e}). "
            "Starting with empty cache."
        )
        return {}

    except Exception as e:

        logger.error(f"Unexpected error loading cache: {e}. Starting fresh.")
        return {}


def save_cache(cache):

    try:

        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)

        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=4, ensure_ascii=False)

        logger.info(f"Cache saved: {len(cache)} entries to '{CACHE_FILE}'.")

    except Exception as e:

        logger.error(f"Failed to save cache: {e}")


def get_cached_result(cache, internship_id):

    result = cache.get(str(internship_id))

    if result:
        logger.debug(f"Cache hit: internship_id={internship_id}")
    else:
        logger.debug(f"Cache miss: internship_id={internship_id}")

    return result


def cache_result(cache, internship_id, result):

    cache[str(internship_id)] = result
    logger.debug(f"Cached result for internship_id={internship_id}")