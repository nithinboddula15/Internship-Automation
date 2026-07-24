# pyrefly: ignore [missing-import]
from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto("https://internshala.com/internships/machine-learning-internship/")

    page.wait_for_timeout(5000)
    
    titles = page.locator(".job-title-href").all_inner_texts()

    for title in titles:
        print(title)        
    
    input("Press Enter to close browser...")

    browser.close()