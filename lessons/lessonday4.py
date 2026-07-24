# pyrefly: ignore [missing-import]
from playwright.sync_api import sync_playwright
import pandas as pd


with sync_playwright() as p:
      
    

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto("https://internshala.com/internships/machine-learning-internship/")

    page.wait_for_timeout(5000)

    cards = page.locator(".individual_internship")

    print(cards.count())

    # Empty list
    internships = []
    new_internships = []

    for i in range(cards.count()):

        print("--------------------------------")
        print("Internship", i + 1)

        card = cards.nth(i)
        internship_id = card.get_attribute("internshipid")
        title = card.locator(".job-title-href").inner_text()
        company = card.locator(".company-name").inner_text()
        location = card.locator(".row-1-item.locations span").first.inner_text()
        stipend = card.locator(".stipend").inner_text()
        duration = card.locator(".row-1-item").nth(2).locator("span").inner_text()
        skills = card.locator(".job_skill").all_inner_texts()

        link = card.locator(".job-title-href").get_attribute("href")
        link = "https://internshala.com" + link

        # Dictionary
        internship = {
            "id": internship_id,
            "title": title,
            "company": company,
            "location": location,
            "stipend": stipend,
            "duration": duration,
            "skills": skills,
            "link": link
        }

        # Add dictionary to list
        new_internships.append(internship)

        # Print as before
        print(internship_id)
        print(title)
        print(company)
        print(location)
        print(stipend)
        print(duration)
        print(skills)
        print(link)
        print("--------------------------------")

    print("\nAll internships collected:\n")
    
    
    df = pd.DataFrame(internships)
    df.to_excel("data/internships.xlsx", index=False)

    input("Press Enter to close browser...")

    browser.close()
