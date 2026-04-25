from itertools import chain

from google import genai
from dotenv import load_dotenv
import os
from memory_manager import save_to_memory, get_recent_memory

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

model = genai.GenerativeModel("gemini-2.5-flash", api_key=API_KEY)

def ai_agent_with_memory(user_input):
    #load last 3 interactions
    past_memory = get_recent_memory(3)

    memory_text = ""
    for item in past_memory:
        memory_text += f"User: {item['user']}\nAgent: {item['agent']}\n\n"
    
    # Build final prompt
    final_prompt = f"""
You are an AI assistant with memory. 
Here is your past memory:
    
   
{memory_text}

Now answer the new user message:

{user_input}
    """

    # Generate the response
    response = model.generate_content(final_prompt)
    answer = response.text

    # Save both user query + AI answer
    save_to_memory(user_input, answer)

    return answer
