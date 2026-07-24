# pyrefly: ignore [missing-import]
from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto("https://internshala.com/internships/machine-learning-internship/")

    page.wait_for_timeout(5000)

    cards = page.locator(".individual_internship")

    card = cards.nth(0)
    title = card.locator(".job-title-href").inner_text()
    print(title)
    company = card.locator(".company_name").inner_text()
    print(company)

    input("Press Enter to close browser...")

    browser.close()
