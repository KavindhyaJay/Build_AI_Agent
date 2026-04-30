from google import genai
from dotenv import load_dotenv
import os
from api_tools import get_current_time

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

MODEL = "gemini-2.5-flash"

def router_agent(query):
    
    # Simple routing logic
    if "time" in query.lower():
        return f"The current time is: {get_current_time()}"
    if "explain" in query.lower():
        explanation = client.models.generate_content(
            model=MODEL,
            contents=f"Answer the following question: {query}"
        ).text
        return explanation
    
    # Default fallback
    response = client.models.generate_content(
        model=MODEL,
        contents=query
    ).text
    return response

if __name__ == "__main__":
    print(router_agent("What is the time now? - router_agent.py:33"))
    print(router_agent("Explain recursion - router_agent.py:34"))