from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="天空為什麼藍的"
)
print(response.text)
