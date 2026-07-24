# pyrefly: ignore [missing-import]
from playwright.sync_api import sync_playwright
import pandas as pd

try:
    old_df = pd.read_excel("data/internships.xlsx")
    existing_ids = old_df["internship_id"].tolist()
except:
    old_df = pd.DataFrame()
    existing_ids = []

allowed_roles = [
    "Data Science",
    "Machine Learning",
    "Artificial Intelligence",
    "AI",
    "Python",
    "Computer Vision",
    "Deep Learning",
    "NLP",
    "Data Analytics",
    "AI Engineer",
    "AI Agent"
]


with sync_playwright() as p:
      
    

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto("https://internshala.com/internships/")

    page.wait_for_timeout(5000)

    cards = page.locator(".individual_internship")

    print(cards.count())

    # Empty list
    new_internships = []

    for i in range(cards.count()):

        card = cards.nth(i)
        internship_id = int(card.get_attribute("internshipid"))
        if internship_id in existing_ids:
            print("Duplicate - Skipping")
            continue
        print("--------------------------------")
        print("Internship", i + 1)
        title = card.locator(".job-title-href").inner_text()
        if not any(role.lower() in title.lower() for role in allowed_roles):
            print("Role not matched - Skipping")
            continue
        company = card.locator(".company-name").inner_text()
        location = card.locator(".row-1-item.locations span").first.inner_text()
        stipend = card.locator(".stipend").inner_text()
        duration = card.locator(".row-1-item").nth(2).locator("span").inner_text()
        skills = card.locator(".job_skill").all_inner_texts()

        link = card.locator(".job-title-href").get_attribute("href")
        link = "https://internshala.com" + link

        # Dictionary
        internship = {
            "internship_id": internship_id,
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

    print(new_internships)
    
    df = pd.DataFrame(new_internships)
    final_df = pd.concat([old_df, df], ignore_index=True)
    final_df.to_excel("data/internships.xlsx", index=False)
    

    input("Press Enter to close browser...")

    browser.close()