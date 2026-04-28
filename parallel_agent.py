from google import genai
from dotenv import load_dotenv
import os
import concurrent.futures

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

MODEL = "gemini-2.5-flash"

def ask_gemini(prompt):
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )
        return response.text   # ✅ IMPORTANT (you missed this)

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    prompts = [
        "Summarize Python in 20 words",
        "Explain AI agent in simple terms",
        "Give a motivational quote",
        "Write 1-line definition of API"
    ]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(ask_gemini, prompts))

    for r in results:
        print("\n__________\n - parallel_agent.py:36", r)