import json
import time

from google import genai
from google.genai.errors import ClientError

from config_local import gemini_api_key
from logger import logger

client = genai.Client(api_key=gemini_api_key)


def classify_title(title):

    prompt = f"""
You are an internship classifier.

The candidate is interested in internships related to the following technical domains.

Accept titles that clearly belong to these domains or are closely related.

Reject marketing, HR, finance, CA, sales, customer support, content writing, operations, business development and other non-technical roles.

- Artificial Intelligence
- Machine Learning
- Deep Learning
- Data Science
- Data Analytics
- Computer Vision
- NLP
- Python Development
- AI Engineering
- LLM
- Generative AI
- AI Agents
- MLOps
- Data Engineering
- Software Development

Internship Title:
{title}

Return ONLY valid JSON.

{{
    "is_relevant": true,
    "reason": ""
}}
"""

    for attempt in range(2):

        try:

            response = client.models.generate_content(
                model="gemini-flash-lite-latest",
                contents=prompt
            )

            text = response.text.strip()

            # Remove markdown if Gemini adds it
            text = text.replace("```json", "")
            text = text.replace("```", "")
            text = text.strip()

            return json.loads(text)

        except json.JSONDecodeError:

            logger.warning(
                f"Title JSON parse failed for '{title}' (Attempt {attempt+1})"
            )

            if attempt == 0:
                time.sleep(2)
                continue

            logger.error(response.text)

            return {
                "is_relevant": False,
                "reason": "JSON parse error"
            }

        except ClientError as e:

            logger.warning(
                f"Gemini API error for '{title}' (Attempt {attempt+1}): {e}"
            )

            if attempt == 0:
                time.sleep(5)
                continue

            return {
                "is_relevant": False,
                "reason": "API error"
            }

        except Exception as e:

            logger.exception(
                f"Unexpected error while classifying '{title}'"
            )

            return {
                "is_relevant": False,
                "reason": "Unknown error"
            }