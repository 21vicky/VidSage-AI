from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

print("Testing Gemini connection...")

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=(
        "Summarize this text in 3 sentences:\n"
        + transcript[:3000]
    )
)

print("\n===== GEMINI RESPONSE =====\n")
print(response.text)
