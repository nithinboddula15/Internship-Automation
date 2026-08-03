import json

from google import genai
from google.genai.errors import ClientError
from config_local import gemini_api_key
from logger import logger

client = genai.Client(api_key=gemini_api_key)


def classify_title(title):
    prompt = f"""
You are an internship classifier.

The candidate wants internships in

- AI
- Machine Learning
- Data Science
- Python
- Deep Learning
- Computer Vision
- NLP
- Data Analytics
- AI Agents
- LLM
- Generative AI

Job Title

{title}

Return ONLY JSON

{{
"is_relevant": true,
"reason":""
}}

"""
    try:
        response = client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=prompt
        )
        return json.loads(response.text)

    except json.JSONDecodeError:
        logger.error(f"Title classifier returned invalid JSON for: '{title}'")
        return {{"is_relevant": False, "reason": "JSON parse error"}}

    except ClientError as e:
        logger.error(f"Gemini API error during title classification: {{e}}")
        return {{"is_relevant": False, "reason": "API error"}}

    except Exception as e:
        logger.error(f"Unexpected error classifying title '{{title}}': {{e}}")
        return {{"is_relevant": False, "reason": "Unknown error"}}