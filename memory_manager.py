import json
import os

MEMORY_FILE = "agent_memory.json"

if not os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, 'w') as f:
        json.dump({"history": []}, f)

def save_to_memory(user_text, agent_response):
    """"Save user + agent messages into log-term memory."""
    with open(MEMORY_FILE, 'r') as f:
        data = json.load(f)

    data["history"].append({
        "user": user_text, 
        "agent": agent_response})

    with open(MEMORY_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def get_recent_memory(n=3):
    """Retrieve last N memory events."""
    with open(MEMORY_FILE, 'r') as f:
        data = json.load(f)

    return data["history"][-n:]