from google import genai
from dotenv import load_dotenv
import os
from memory_manager import save_to_memory, get_recent_memory

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

MODEL = "gemini-2.5-flash"

def chain(prompt):

    #step 1: ask agent to brake doen the task
    step_1 = client.models.generate_content(
        model=MODEL,
        contents=f"Break this task into clear steps: \n{prompt}"
    ).text
        
    print("\nStep 1  Breakdown:\n  agent_with_memory.py:17 - prompt_chain_agent.py:21", step_1)
    
    #step 2: ask agent to complete the reasoning
    step_2 = client.models.generate_content(
        model=MODEL,
        contents=f"Based on the steps, give the detailed explanation: \nSteps: {step_1}\nTask: {prompt}"
    ).text
    print("\n[Explanation]  agent_with_memory.py:23 - prompt_chain_agent.py:28", step_2)

    #step 3 Ask agent for final summary
    step_3 = client.models.generate_content(
        model=MODEL,
        contents=f"Summarize the final answer in simple words: \nExplanation: {step_2}\nTask: {prompt}"
    ).text
    print("\n[Summary]  agent_with_memory.py:29 - prompt_chain_agent.py:35", step_3)

    return step_3

if __name__ == "__main__":
    chain("Explain Python decorators with an example.")