from dotenv import load_dotenv
from google import genai
import os
from api_tools import get_current_time

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Create client
client = genai.Client(api_key=API_KEY)

MODEL = "gemini-2.5-flash"

def chat_with_agent(prompt):
    if "time" in prompt.lower():
        real_time = get_current_time()
        prompt += f"\nReal-time data: The current time is {real_time}"

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )
        return response.text

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    print(chat_with_agent("What is the current time right now? - agent_api_call.py:30"))