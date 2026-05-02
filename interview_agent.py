# from google import genai
# from streamlit import feedback
# from dotenv import load_dotenv
# import os
# import time
# import json

# from memory_manager import save_interview_record,save_strength,save_weakness
# from tools import(
#     keyword_match_score,
#     generate_score,
#     improvement_tips,
#     classify_strength_or_weakness,
#     short_feedback
# )

# load_dotenv()
# API_KEY = os.getenv("GEMINI_API_KEY")

# client = genai.Client(api_key=API_KEY)

# MODEL = "gemini-1.5-flash"
# MOCK_MODE = True

# #-------------------------------
# #GENERATE INTERVIEW QUESTIONS
# #---------------------------------

# import time # Add this to your imports at the top

# def generate_questions(role):
#     if MOCK_MODE:
#         time.sleep(1) # Simulate network delay
#         return f"[MOCK QUESTION] Can you explain a complex data concept you solved as a {role}?"
#     prompt = f"""
#     Act as a professional interviewer for the role: {role}.
#     Ask one realistic interview question.
#     DO NOT include answers, hints, or any explanation. Only provide the question.
#     Just ask the question.
#     """
    
#     max_retries = 3
#     for attempt in range(max_retries):
#         try:
#             response = client.models.generate_content(
#                 model=MODEL,
#                 contents=prompt
#             )
#             return response.text.strip()
            
#         except Exception as e:
#             error_msg = str(e)
#             # If it's a 503 (Unavailable) or 429 (Too Many Requests), wait and retry
#             if "503" in error_msg or "429" in error_msg:
#                 wait_time = 2 ** attempt  # Waits 1s, then 2s, then 4s
#                 print(f"\n[System] API busy. Retrying in {wait_time} seconds... - interview_agent.py:56")
#                 time.sleep(wait_time)
#             else:
#                 # If it's a different error (like bad API key), fail immediately
#                 return f"Error: {error_msg}"
                
#     # If it fails all 3 times
#     return "Error: Unable to reach the AI after multiple attempts. Please try again later."
    
# #-------------------------------
# #ANALYZE THE USER ANSWER\
# #---------------------------------

# def analyze_answer(role, answer, role_data):
#     keywords = role_data["keywords"]
#     difficulty = role_data["difficulty"]

#     k_score = keyword_match_score(answer, keywords)
#     final_score = generate_score(k_score, difficulty)
#     improvement = improvement_tips(keywords, answer)
#     brief = short_feedback(final_score)
#     analysis_prompt = f"""
# You are an HR expert & senior interviewer.analyze_answer
# Evaluate this answer for the role of {role}:
# Candidate's answer: {answer}

# score: {final_score}/10
# Strengths.Weakness based on the keywords:{improvement}

# Provide:
# 1. A short analysis (2-3 lines)
# 2. One sentence on how a recruiter will perceive this answer
# 3. One actionable improvement tip
# Make feedback helpful but not harsh.
# """
    
#      # 🔥 SAFE API CALL (FIX)
#     try:
#         response = client.models.generate_content(
#             model=MODEL,
#             contents=analysis_prompt
#         )
#         ai_feedback = response.text

#     except Exception as e:
#         ai_feedback = f"AI temporarily unavailable: {str(e)}"
#     if MOCK_MODE:
#         time.sleep(1) # Simulate network delay
#         return {
#                 "score": final_score,
#                 "improvement_tips": improvement,
#                 "brief_feedback": brief,
#                 "ai_feedback": ai_feedback
#         }

import os
import time
import json
from google import genai
from dotenv import load_dotenv

from memory_manager import save_interview_record, save_strength, save_weakness

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

# Use the latest stable 2.0 flash model
MODEL =  "gemini-2.5-flash"  

# Toggle this to False when you are ready to test the real AI
MOCK_MODE = False

#-------------------------------
# GENERATE INTERVIEW QUESTIONS
#---------------------------------
def generate_questions(role):
    # Immediate return if mock mode is on
    if MOCK_MODE:
        time.sleep(1) # Simulate network delay
        mock_questions = [
            f"[MOCK Q1] What is the most challenging project you've worked on as a {role}?",
            f"[MOCK Q2] How do you handle disagreements with your team regarding technical decisions?",
            f"[MOCK Q3] Can you explain a complex data concept you solved as a {role}?",
            f"[MOCK Q4] Walk me through your debugging process when a production system goes down."
        ]
        return random.choice(mock_questions)
        
    prompt = f"""
    Act as a professional interviewer for the role: {role}.
    Ask one realistic interview question.
    DO NOT include answers, hints, or any explanation. Only provide the question.
    Just ask the question.
    """
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt
            )
            return response.text.strip()
            
        except Exception as e:
            error_msg = str(e)
            # If it's a 503 (Unavailable) or 429 (Too Many Requests), wait and retry
            if "503" in error_msg or "429" in error_msg:
                wait_time = 2 ** attempt  # Waits 1s, then 2s, then 4s
                print(f"\n[System] API busy. Retrying in {wait_time} seconds... - interview_agent.py:166")
                time.sleep(wait_time)
            else:
                # If it's a different error (like bad API key), fail immediately
                return f"Error: {error_msg}"
                
    # If it fails all 3 times
    return "Error: Unable to reach the AI after multiple attempts. Please try again later."
    
#-------------------------------
# ANALYZE THE USER ANSWER
#---------------------------------
def analyze_answer(role, answer, role_data):
    # Immediate return if mock mode is on
    if MOCK_MODE:
        time.sleep(1) # Simulate network delay
        return {
            "score": 9,
            "improvement_tips": "Try to mention specific scaling metrics next time.",
            "brief_feedback": "Excellent explanation of a difficult concept!",
            "ai_feedback": "[MOCK AI FEEDBACK] This is a simulated response. Your answer successfully covered the core principles. You sound like a senior developer!"
        }

    # The new LLM-as-a-judge prompt
    analysis_prompt = f"""
    You are an expert technical interviewer for the role of {role}.
    Evaluate this candidate's answer based on technical accuracy, depth, and clarity.
    
    Candidate's answer: {answer}
    
    You MUST respond with a raw JSON object (no markdown formatting) containing exactly these keys:
    {{
        "score": <an integer between 1 and 10>,
        "improvement_tips": "<short sentence on what they missed>",
        "brief_feedback": "<one short encouraging sentence>",
        "ai_feedback": "<2-3 sentences of detailed technical feedback>"
    }}
    """
    
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=analysis_prompt
        )
        
        raw_text = response.text.strip()
        
        # Safety cleaner: Remove markdown code blocks if the AI accidentally adds them
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        elif raw_text.startswith("```"):
            raw_text = raw_text[3:]
            
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
            
        feedback_dict = json.loads(raw_text.strip())
        return feedback_dict

    except json.JSONDecodeError:
        # Handles cases where the AI failed to output valid JSON
        return {
            "score": 0,
            "improvement_tips": "AI formatting error.",
            "brief_feedback": "System could not parse the score.",
            "ai_feedback": f"Raw response was not JSON: {response.text}"
        }
    except Exception as e:
        # Handles API down/unavailable errors
        return {
            "score": 0,
            "improvement_tips": "N/A",
            "brief_feedback": "API temporarily unavailable.",
            "ai_feedback": f"Error: {str(e)}"
        }