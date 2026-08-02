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

result = semantic_match(
    resume,
    internship
)

print(result)

print(type(result))