from matcher import semantic_match

resume = """
Python
Machine Learning
Pandas
Power BI
"""

internship = {
    "title": "Data Scientist",
    "company": "Google",
    "description": """
Looking for Python,
Machine Learning,
Statistics,
SQL,
Docker
"""
}

print(
    semantic_match(
        resume,
        internship
    )
)