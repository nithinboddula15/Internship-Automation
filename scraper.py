# pyrefly: ignore [missing-import]
from playwright.sync_api import sync_playwright, TimeoutError

import time

from logger import logger
from filters import role_matches, recent_post
from matcher import match_resume_to_internship
from ai_cache import load_cache, save_cache, get_cached_result, cache_result
from career import MAX_POSTED_DAYS

MAX_EMPTY_PAGES = 5


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


def close_browser(playwright, browser):

    input("Press Enter to close browser...")
    browser.close()
    playwright.stop()

    logger.info("Browser closed.")


# ==================================================
# Page navigation
# ==================================================

def open_page(page, page_number):

    if page_number == 1:
        url = "https://internshala.com/internships/machine-learning-internship/"
    else:
        url = f"https://internshala.com/internships/machine-learning-internship/page-{page_number}/"

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
            time.sleep(3)

        except Exception as e:

            logger.error(f"Error opening page {page_number}: {e}. Attempt {attempt}/3.")
            time.sleep(3)

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

    return {
        "internship_id": internship_id,
        "title": title,
        "posted_time": posted_time
    }


# pyrefly: ignore [parse-error]
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

def scrape_page(page, browser, existing_ids, resume_text, resume_skills, cache):

    cards = get_cards(page)
    total_cards = cards.count()
    new_internships = []

    logger.info(f"Found {total_cards} cards on this page.")

    for i in range(total_cards):

        card = cards.nth(i)

        try:

            # ---------- Basic Info ----------
            basic = extract_basic_info(card)

            # Duplicate check
            if basic["internship_id"] in existing_ids:
                logger.info(f"Skipped '{basic['title']}' - Duplicate.")
                continue

            # Role filter
            if not role_matches(basic["title"]):
                logger.info(f"Skipped '{basic['title']}' - Role not matched.")
                continue

            # Posted time filter
            if basic["posted_time"] is None:
                logger.info(f"Skipped card {i} - No posted time.")
                continue

            if not recent_post(basic["posted_time"]):
                logger.info(
                    f"Skipped '{basic['title']}' - "
                    f"Posted {basic['posted_time']} (too old)."
                )
                continue

            # ---------- Full Extraction ----------
            logger.info(f"Processing: '{basic['title']}'")
            internship = extract_full_info(card, browser)

            # ---------- AI Match (with cache) ----------
            cached_result = get_cached_result(cache, internship["internship_id"])

            if cached_result:

                logger.info(
                    f"Cache hit for '{internship['title']}' "
                    f"(id={internship['internship_id']})"
                )
                result = cached_result

            else:

                logger.info(
                    f"Calling Gemini for '{internship['title']}' "
                    f"(id={internship['internship_id']})..."
                )

                result = match_resume_to_internship(
                    resume_skills=resume_skills,
                    internship_skills=internship["skills"],
                    resume_text=resume_text,
                    internship=internship
                )

                if result["recommendation_status"] not in ("API Error", "Unknown Error"):
                    cache_result(cache, internship["internship_id"], result)
                    logger.info("Result cached.")
                else:
                    logger.warning(
                        f"Result NOT cached due to status: "
                        f"{result['recommendation_status']}"
                    )

            # ---------- Attach results ----------
            internship["match_score"] = result["match_score"]
            internship["matched_skills"] = result["matched_skills"]
            internship["missing_skills"] = result["missing_skills"]
            internship["internship_skills"] = result.get("internship_skills", [])
            internship["recommendation_status"] = result["recommendation_status"]
            internship["ai_reason"] = result["ai_reason"]
            internship["application_advice"] = result["application_advice"]

            new_internships.append(internship)

            logger.info(
                f"✔ '{internship['title']}' | {internship['company']} | "
                f"Score: {internship['match_score']}% | "
                f"{internship['recommendation_status']}"
            )

        except Exception as e:

            logger.error(f"Error processing card {i}: {e}", exc_info=True)
            continue

    logger.info(f"Page done. {len(new_internships)} internship(s) collected.")
    return new_internships


# ==================================================
# Main entry point
# ==================================================

def scrape_internships(existing_ids, resume_text, resume_skills):

    logger.info("Scraper started.")
    logger.info(f"Existing IDs in database: {len(existing_ids)}")

    cache = load_cache()
    logger.info(f"Cache loaded. {len(cache)} cached results.")

    playwright, browser, page = open_browser()

    all_new_internships = []
    page_number = 1
    empty_pages = 0

    try:

        while True:

            success = open_page(page, page_number)

            if not success:
                logger.error(
                    f"Could not open page {page_number}. Stopping scraper."
                )
                break

            page_internships = scrape_page(
                page,
                browser,
                existing_ids,
                resume_text,
                resume_skills,
                cache
            )

            # ---------- Empty page tracking ----------
            if len(page_internships) == 0:

                empty_pages += 1

                logger.info(
                    f"Page {page_number}: No suitable internships. "
                    f"Empty streak: {empty_pages}/{MAX_EMPTY_PAGES}"
                )

            else:

                empty_pages = 0
                all_new_internships.extend(page_internships)

                logger.info(
                    f"Page {page_number}: +{len(page_internships)} internship(s). "
                    f"Total so far: {len(all_new_internships)}"
                )

            if empty_pages >= MAX_EMPTY_PAGES:

                logger.info(
                    f"{MAX_EMPTY_PAGES} consecutive empty pages. Stopping scraper."
                )
                break

            page_number += 1

    except Exception as e:

        logger.error(f"Scraper crashed: {e}", exc_info=True)

    finally:

        save_cache(cache)
        logger.info(f"Cache saved. {len(cache)} total entries.")

        close_browser(playwright, browser)

    logger.info(
        f"Scraper finished. Total new internships collected: "
        f"{len(all_new_internships)}"
    )

    return all_new_internships
