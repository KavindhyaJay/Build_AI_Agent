import json
import os

MEMORY_FILE = "interview_memory.json"

if not os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, 'w') as f:
        json.dump({"history": [], "strengths": [], "weaknesses": []}, f)

def save_interview_record(role, question, user_answer, feedback):
    """"Save one Q&A record to log-term memory."""
    with open(MEMORY_FILE, 'r') as f:
        data = json.load(f)

    data["history"].append({
        "role": role,
        "question": question,
        "user_answer": user_answer,
        "feedback": feedback
    })

    with open(MEMORY_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def save_strength(strength):
    """Store user's strong areas."""
    with open(MEMORY_FILE, 'r') as f:
        data = json.load(f)

    data["strengths"].append(strength)

    with open(MEMORY_FILE, 'w') as f:
        json.dump(data, f, indent=4)


def save_weakness(weakness):
    """Store user's weak areas for future improvement."""
    with open(MEMORY_FILE, 'r') as f:
        data = json.load(f)

    data["weaknesses"].append(weakness)

    with open(MEMORY_FILE, 'w') as f:
        json.dump(data, f, indent=4)


def get_memory_summary():
    """Retrieve memory for personalized reports."""
    with open(MEMORY_FILE, 'r') as f:
        data = json.load(f)

    