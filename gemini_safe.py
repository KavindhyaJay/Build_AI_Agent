import time
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)
MODEL = "gemini-2.5-flash"

def safe_generate(prompt, retries=3, delay=3):
    for i in range(retries):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            print(f"[Retry {i+1}] API busy... - gemini_safe.py:21")
            time.sleep(delay)

    return "AI unavailable. Try again later."