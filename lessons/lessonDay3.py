# pyrefly: ignore [missing-import]
from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto("https://internshala.com/internships/machine-learning-internship/")

    page.wait_for_timeout(5000)

    cards = page.locator(".individual_internship")

    print(f"Total Internships: {cards.count()}")

    for i in range(cards.count()):

        print("=" * 60)
        print(f"Internship {i+1}")
        print("=" * 60)

        card = cards.nth(i)

        # Title
        title = card.locator(".job-title-href").inner_text().strip()

        # Company
        company = card.locator(".company-name").inner_text().strip()

        # Location
        location = card.locator(".row-1-item.locations span").first.inner_text().strip()

        # Stipend
        stipend = card.locator(".stipend").inner_text().strip()

        # Duration
        duration = card.locator(".row-1-item").nth(2).locator("span").inner_text().strip()

        # Skills
        skills = card.locator(".job_skill").all_inner_texts()

        # Apply Link
        link = card.locator(".job-title-href").get_attribute("href")

        if link:
            link = "https://internshala.com" + link

        print(f"Title     : {title}")
        print(f"Company   : {company}")
        print(f"Location  : {location}")
        print(f"Stipend   : {stipend}")
        print(f"Duration  : {duration}")
        print(f"Skills    : {', '.join(skills)}")
        print(f"Apply Link: {link}")

        print()

    input("Press Enter to close browser...")

    browser.close()