from google import genai
from config_local import gemini_api_key

client = genai.Client(api_key=gemini_api_key)

print("Using model: models/gemini-3.5-flash")

response = client.models.generate_content(
    model="models/gemini-3.5-flash",
    contents="Reply with only the word OK"
)

print(response.text)