import json
import os

MEMORY_FILE = "interview_memory.json"

def _load_data():
    """Helper function to safely load data and ensure all keys exist."""
    # If the file doesn't exist at all, return a fresh dictionary
    if not os.path.exists(MEMORY_FILE):
        return {"history": [], "strengths": [], "weaknesses": []}
        
    try:
        with open(MEMORY_FILE, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        # If the file is corrupted or empty, start fresh
        data = {}
        
    # BACKWARDS COMPATIBILITY: 
    # If it's an old file missing the new keys, add them safely!
    if "history" not in data: 
        data["history"] = []
    if "strengths" not in data: 
        data["strengths"] = []
    if "weaknesses" not in data: 
        data["weaknesses"] = []
        
    return data

def _save_data(data):
    """Helper function to save data back to the JSON file."""
    with open(MEMORY_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def save_interview_record(role, question, user_answer, feedback):
    """Save one Q&A record to long-term memory."""
    data = _load_data()
    
    data["history"].append({
        "role": role,
        "question": question,
        "user_answer": user_answer,
        "feedback": feedback
    })
    
    _save_data(data)

def save_strength(strength):
    """Store user's strong areas."""
    data = _load_data()
    data["strengths"].append(strength)
    _save_data(data)

def save_weakness(weakness):
    """Store user's weak areas for future improvement."""
    data = _load_data()
    data["weaknesses"].append(weakness)
    _save_data(data)

def get_memory_summary():
    """Retrieve memory for personalized reports."""
    return _load_data()