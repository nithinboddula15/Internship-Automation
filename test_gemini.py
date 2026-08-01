from google import genai
from config_local import gemini_api_key

client = genai.Client(api_key=gemini_api_key)

response = client.models.generate_content(
    model="models/gemini-3.5-flash",
    contents="Say hello in one sentence."
)

print(response.text)