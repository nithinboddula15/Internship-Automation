# pyrefly: ignore [missing-import]
from playwright.sync_api import sync_playwright

from filters import role_matches
from filters import recent_post

def open_browser():

    playwright = sync_playwright().start()

    browser = playwright.chromium.launch(headless=False)

    page = browser.new_page()

    return playwright, browser, page

def close_browser(playwright, browser):

    input("Press Enter to close browser...")

    browser.close()

    playwright.stop()

def open_page(page, page_number):

    if page_number == 1:
        url = "https://internshala.com/internships/"
    else:
        url = f"https://internshala.com/internships/page-{page_number}/"

    print(f"\nOpening Page {page_number}")

    page.goto(url, wait_until="domcontentloaded")

    page.locator(".individual_internship").first.wait_for(timeout=10000)


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


def extract_internship(card):

    internship_id = int(card.get_attribute("internshipid"))

    title = card.locator(".job-title-href").inner_text()

    company = card.locator(".company-name").inner_text()

    location = card.locator(
        ".row-1-item.locations span"
    ).first.inner_text()

    stipend = card.locator(".stipend").inner_text()

    duration = get_duration(card)

    skills = card.locator(".job_skill").all_inner_texts()

    link = card.locator(".job-title-href").get_attribute("href")

    link = "https://internshala.com" + link

    return {
        "internship_id": internship_id,
        "title": title,
        "company": company,
        "location": location,
        "stipend": stipend,
        "duration": duration,
        "skills": skills,
        "link": link
    }

def scrape_page(page, existing_ids):

    cards = get_cards(page)

    new_internships = []

    for i in range(cards.count()):

        card = cards.nth(i)

        internship = extract_internship(card)

        if internship["internship_id"] in existing_ids:
            print("Duplicate - Skipping")
            continue

        if not role_matches(internship["title"]):
            print("Role not matched")
            continue

        posted_time = get_posted_time(card)

        if posted_time is None:
            continue

        if not recent_post(posted_time):
            print("Old Internship")
            continue

        new_internships.append(internship)

        print("--------------------------------")
        print(internship["title"])
        print(internship["company"])
        print(internship["location"])
        print("--------------------------------")

    return new_internships


def scrape_internships(existing_ids):

    playwright, browser, page = open_browser()

    all_new_internships = []

    page_number = 1

    while True:

        open_page(page, page_number)

        page_internships = scrape_page(page, existing_ids)

        if len(page_internships) == 0:
            print("No new internships on this page.")
            break

        all_new_internships.extend(page_internships)

        page_number += 1

    close_browser(playwright, browser)

    return all_new_internships