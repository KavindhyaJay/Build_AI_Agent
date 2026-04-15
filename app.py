from dotenv import load_dotenv
from google import genai
import os

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("Error: No API key found - app.py:11")
    exit()

# Create client (NEW method)
client = genai.Client(api_key=API_KEY)

def chat_with_agent(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        print("\nAI Response:\n - app.py:23", response.text)

    except Exception as e:
        print("\nError: - app.py:26", str(e), "")

if __name__ == "__main__":
    chat_with_agent("Tell me a funny AI joke in one sentence")