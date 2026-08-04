# pyrefly: ignore [missing-import]
from playwright.sync_api import sync_playwright, TimeoutError

import time

from logger import logger
from matcher import match_resume_to_internship
from cache.ai_cache import load_cache, save_cache, get_cached_result, cache_result
from career import MAX_EMPTY_PAGES
RETRY_DELAY = 3  # seconds

from filters import (
    quick_filter,
    recent_post,
    skill_overlap
)

from title_classifier import classify_title
from cache.title_cache import (
    load_title_cache,
    save_title_cache,
    get_cached_title,
    cache_title
)


# ==================================================
# Browser helpers
# ==================================================

def open_browser():

    logger.info("Launching browser...")

    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()

    logger.info("Browser launched.")

    return playwright, browser, page


def close_browser(playwright, browser, pause=False):

    if pause:
        input("Press Enter to close browser...")
    browser.close()
    playwright.stop()

    logger.info("Browser closed.")


# ==================================================
# Page navigation
# ==================================================

def open_page(page, page_number):

    if page_number == 1:
        url = "https://internshala.com/internships/ai-agent-development,artificial-intelligence-ai,cloud-computing,data-science,java,machine-learning,python-django,software-development-internship/"
    else:
        url = f"https://internshala.com/internships/ai-agent-development,artificial-intelligence-ai,cloud-computing,data-science,java,machine-learning,python-django,software-development-internship/page-{page_number}/"

    logger.info(f"Opening Page {page_number}: {url}")

    for attempt in range(1, 4):

        try:

            page.goto(url, wait_until="domcontentloaded", timeout=20000)
            page.locator(".individual_internship").first.wait_for(timeout=10000)

            logger.info(f"Page {page_number} loaded successfully.")
            return True

        except TimeoutError:

            logger.warning(
                f"Timeout on page {page_number}. "
                f"Attempt {attempt}/3. Retrying..."
            )
            time.sleep(RETRY_DELAY)

        except Exception as e:

            logger.error(f"Error opening page {page_number}: {e}. Attempt {attempt}/3.")
            time.sleep(RETRY_DELAY)

    logger.error(f"Failed to open page {page_number} after 3 attempts.")
    return False


# ==================================================
# Card helpers
# ==================================================

def get_cards(page):

    return page.locator(".individual_internship")


def get_posted_time(card):

    posted_locator = card.locator(".status-success span")

    if posted_locator.count() == 0:
        return None

    posted_time = posted_locator.first.text_content()

    if not posted_time:
        return None

    return posted_time.strip().lower()


def get_duration(card):

    row_items = card.locator(".row-1-item")

    if row_items.count() > 2:
        return row_items.nth(2).locator("span").inner_text()
    elif row_items.count() > 1:
        return row_items.nth(1).locator("span").inner_text()

    return "Not Specified"


# ==================================================
# Info extractors
# ==================================================

def extract_basic_info(card):

    internship_id = int(card.get_attribute("internshipid"))
    title = card.locator(".job-title-href").inner_text().lower()
    posted_time = get_posted_time(card)
    skills = card.locator(".job_skill").all_inner_texts()

    return {
        "internship_id": internship_id,
        "title": title,
        "posted_time": posted_time,
        "skills": skills if skills else [], 
    }


def extract_full_info(card, browser):

    internship_id = int(card.get_attribute("internshipid"))
    title = card.locator(".job-title-href").inner_text()
    company = card.locator(".company-name").inner_text()
    location = card.locator(".row-1-item.locations span").first.inner_text()
    stipend = card.locator(".stipend").inner_text()
    duration = get_duration(card)
    skills = card.locator(".job_skill").all_inner_texts()

    link = card.locator(".job-title-href").get_attribute("href")
    link = "https://internshala.com" + link

    description = get_internship_description(browser, link)

    return {
        "internship_id": internship_id,
        "title": title,
        "company": company,
        "location": location,
        "stipend": stipend,
        "duration": duration,
        "skills": skills,
        "link": link,
        "description": description
    }


def get_internship_description(browser, link):

    new_page = browser.new_page()
    description = ""

    try:

        new_page.goto(link, wait_until="domcontentloaded", timeout=15000)
        new_page.wait_for_timeout(1000)

        description = "\n".join(
            new_page.locator(".text-container").all_inner_texts()
        )

        logger.info(f"Description fetched for: {link}")

    except TimeoutError:

        logger.warning(f"Timeout fetching description for: {link}")

    except Exception as e:

        logger.error(f"Description fetch error for {link}: {e}")

    finally:

        new_page.close()

    return description


# ==================================================
# Page scraper
# ==================================================

def scrape_page(
    page,
    browser,
    existing_ids,
    resume_text,
    resume_skills,
    cache,
    title_cache,
    stats
):

    cards = get_cards(page)
    total_cards = cards.count()
    new_internships = []

    logger.info(f"Found {total_cards} cards on this page.")

    stats["cards_seen"] += total_cards

    for i in range(total_cards):

        card = cards.nth(i)

        try:

            # ===================================
            # BASIC INFO
            # ===================================

            basic = extract_basic_info(card)

            if basic is None:
                continue

            # -----------------------------------
            # Duplicate
            # -----------------------------------

            if basic["internship_id"] in existing_ids:

                stats["duplicates"] += 1

                logger.info(
                    f"Skipped '{basic['title']}' - Duplicate."
                )

                continue

            # -----------------------------------
            # Quick Filter
            # -----------------------------------

            filter_result = quick_filter(basic["title"])

            if filter_result is False:

                stats["quick_filter"] += 1

                logger.info(
                    f"Skipped '{basic['title']}' - Negative filter."
                )

                continue

            elif filter_result is True:

                logger.info(
                    f"Quick filter passed: '{basic['title']}'"
                )

            else:

                cached = get_cached_title(title_cache, basic["title"])

                if cached:

                    logger.info(
                        f"Title cache hit: '{basic['title']}'"
                    )

                    relevant = cached["is_relevant"]

                else:

                    logger.info(
                        f"AI classifying title: '{basic['title']}'"
                    )

                    result = classify_title(basic["title"])

                    cache_title(title_cache, basic["title"], result)

                    relevant = result["is_relevant"]

                if not relevant:

                    logger.info(
                        f"Skipped '{basic['title']}' - AI marked as irrelevant."
                    )
                    continue
    

            # -----------------------------------
            # Posted Time
            # -----------------------------------

            if basic["posted_time"] is None:

                logger.info(
                    f"Skipped card {i} - No posted time."
                )

                continue

            if not recent_post(basic["posted_time"]):

                stats["old_posts"] += 1

                logger.info(
                    f"Skipped '{basic['title']}' - Too old."
                )

                continue

            # -----------------------------------
            # Skill Overlap
            # -----------------------------------

            if not skill_overlap(
                basic["skills"],
                resume_skills
            ):

                stats["skill_filter"] += 1

                logger.info(
                    f"Skipped '{basic['title']}' - No matching skills."
                )

                continue

            # ===================================
            # FULL EXTRACTION
            # ===================================

            logger.info(
                f"Processing: '{basic['title']}'"
            )
            

            internship = extract_full_info(
                card,
                browser
            )
           
            # ===================================
            # AI CACHE
            # ===================================

           

            cache_key = get_cache_key(internship)

            cached_result = get_cached_result(cache, cache_key)

            if cached_result:

                stats["cache_hits"] += 1

                logger.info(
                    f"Cache hit for '{internship['title']}' "
                    f"(id={internship['internship_id']})"
                )

                result = cached_result

            else:

                stats["gemini_calls"] += 1

                logger.info(
                    f"Calling Gemini for "
                    f"'{internship['title']}' "
                    f"(id={internship['internship_id']})..."
                )

                result = match_resume_to_internship(
                    resume_skills=resume_skills,
                    internship_skills=internship["skills"],
                    resume_text=resume_text,
                    internship=internship
                )

                status = result.get(
                    "recommendation_status",
                    ""
                )

                if status in (
                    "API Error",
                    "Parse Error",
                    "Unknown Error"
                ):

                    logger.warning("Retrying Gemini...")

                    time.sleep(3)

                    result = match_resume_to_internship(
                        resume_skills=resume_skills,
                        internship_skills=internship["skills"],
                        resume_text=resume_text,
                        internship=internship
                    )

                    status = result.get("recommendation_status", "")

                if status not in (
                    "API Error",
                    "Unknown Error",
                    "Parse Error"
                ):

                    cache_result(cache, cache_key, result)
                    

                    logger.info("Result cached.")

                else:

                    logger.warning(
                        f"Result NOT cached due to status: {status}"
                    )

                    result = {
    "match_score": 0,
    "recommendation_status": "API Error",
    "matched_skills": [],
    "missing_skills": [],
    "strengths": [],
    "weaknesses": [],
    "application_advice": ""
}

                    logger.warning("Gemini unavailable.")

                    

            # ===================================
            # STORE RESULTS
            # ===================================

            internship["match_score"] = result.get(
                "match_score",
                0
            )

            internship["matched_skills"] = result.get(
                "matched_skills",
                []
            )

            internship["missing_skills"] = result.get(
                "missing_skills",
                []
            )

            internship["internship_skills"] = result.get(
                "internship_skills",
                []
            )

            internship["recommendation_status"] = result.get(
                "recommendation_status",
                "Unknown Error"
            )

            internship["strengths"] = result.get(
                "strengths",
                []
            )

            internship["weaknesses"] = result.get(
                "weaknesses",
                []
            )

            internship["application_advice"] = result.get(
                "application_advice",
                ""
            )

            new_internships.append(internship)

            stats["new_internships"] += 1

            logger.info(
                f"✔ '{internship['title']}' | "
                f"{internship['company']} | "
                f"Score: {internship['match_score']}% | "
                f"{internship['recommendation_status']}"
            )

        except Exception as e:

            logger.error(
                f"Error processing card {i}: {e}",
                exc_info=True
            )

            continue

    logger.info(
        f"Page done. {len(new_internships)} internship(s) collected."
    )

    return new_internships

# ==========================================
# Cache helper
# ==========================================
def get_cache_key(internship):

    internship_id = internship.get("internship_id")

    if internship_id:
        return str(internship_id)

    return (
        internship["title"].strip().lower()
        + "|"
        + internship["company"].strip().lower()
    )

# ==================================================
# Main entry point
# ==================================================

def scrape_internships(existing_ids, resume_text, resume_skills):

    logger.info("Scraper started.")
    logger.info(f"Existing IDs in database: {len(existing_ids)}")

    # -----------------------------
    # Load caches
    # -----------------------------
    cache = load_cache()
    logger.info(f"Cache loaded. {len(cache)} cached AI results.")

    title_cache = load_title_cache()
    logger.info(f"Title cache loaded. {len(title_cache)} entries.")

    # -----------------------------
    # Statistics
    # -----------------------------
    stats = {
        "cards_seen": 0,
        "duplicates": 0,
        "quick_filter": 0,
        "old_posts": 0,
        "skill_filter": 0,
        "cache_hits": 0,
        "gemini_calls": 0,
        "new_internships": 0,
    }

    playwright, browser, page = open_browser()

    all_new_internships = []

    page_number = 1
    empty_pages = 0

    try:

        while True:

            success = open_page(page, page_number)

            # Skip failed page instead of stopping
            if not success:
                logger.warning(
                    f"Skipping page {page_number} because it could not be opened."
                )

                page_number += 1
                continue

            page_new = scrape_page(
                page=page,
                browser=browser,
                existing_ids=existing_ids,
                resume_text=resume_text,
                resume_skills=resume_skills,
                cache=cache,
                title_cache=title_cache,
                stats=stats
            )

            if page_new:

                all_new_internships.extend(page_new)

                existing_ids.update(
                    internship["internship_id"]
                    for internship in page_new
                )

                # Save caches after every successful page
                save_cache(cache)
                save_title_cache(title_cache)

                logger.info("Caches auto-saved.")

                empty_pages = 0

                logger.info(
                    f"Page {page_number}: +{len(page_new)} internship(s). "
                    f"Total so far: {len(all_new_internships)}"
                )

            else:

                empty_pages += 1

                logger.info(
                    f"Page {page_number}: No suitable internships. "
                    f"Empty streak: {empty_pages}/{MAX_EMPTY_PAGES}"
                )

                if empty_pages >= MAX_EMPTY_PAGES:

                    logger.info(
                        "Reached maximum empty pages. Stopping scraper."
                    )
                    break

            page_number += 1

    finally:

        save_cache(cache)
        save_title_cache(title_cache)

        close_browser(playwright, browser)

        logger.info("Scraper finished.")

    # -----------------------------
    # Final Statistics
    # -----------------------------
    logger.info("=" * 60)
    logger.info("SCRAPING SUMMARY")
    logger.info("=" * 60)

    logger.info(f"Cards Seen          : {stats['cards_seen']}")
    logger.info(f"Duplicates          : {stats['duplicates']}")
    logger.info(f"Quick Filter Reject : {stats['quick_filter']}")
    logger.info(f"Old Posts           : {stats['old_posts']}")
    logger.info(f"Skill Filter Reject : {stats['skill_filter']}")
    logger.info(f"Cache Hits          : {stats['cache_hits']}")
    logger.info(f"Gemini Calls        : {stats['gemini_calls']}")
    logger.info(f"New Internships     : {stats['new_internships']}")

    logger.info("=" * 60)

    logger.info(
        f"Scraper finished. Total new internships collected: "
        f"{len(all_new_internships)}"
    )

    for key, value in stats.items():
        logger.info(f"{key:20}: {value}")

    return all_new_internships
