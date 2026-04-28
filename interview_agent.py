from google import genai
from dotenv import load_dotenv
import os

from memory_manager import save_interview_record,save_strength,save_weakness
from tools import(
    keyword_match_score,
    generate_score,
    improvemnt_tips,
    classify_strength_or_weakness,
    short_feedback
)

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

MODEL = "gemini-2.5-flash"

#-------------------------------
#GENERATE INTERVIEW QUESTIONS
#---------------------------------

def generate_questions(role):
    prompt = f"""
    Act as a professinal interviewer for the role: {role}.
    Ask one realistic interview question.
    DO NOT include answers, hints, or any explanation. Only provide the question.
    Just ask the question.
    """
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )
        return response.text.strip().split("\n")
    except Exception as e:
        return f"Error: {str(e)}"
    
#-------------------------------
#ANALYZE THE USER ANSWER\
#---------------------------------

def analyze_answer(role, answer, role_date):
    keywords = role_data["keywords"]
    difficulty = role_data["difficulty"]

    k_score = keyword_match_score(answer, keywords)
    final_score = generate_score(k_score, difficulty)
    improvement = improvemnt_tips(answer, keywords)
    brief = short_feedback(final_score)
    analysis_prompt = f"""
You are an HR expert & senior interviewer.analyze_answer
Evaluate this answer for the role of {rile}:
Candidate's answer: {answer}

score: {final_score}/10
Strengths.Weakness based on the keywords:
{improvement}

Provide:
1. A short analysis (2-3 lines)
2. One sentence on how a recruiter will perceive this answer
3. One actionable improvement tip
Make feedback helpful but not harsh.
"""
    ai_feedback = model.generate_content(analysis_prompt).text.strip()  

    category = classify_strength_or_weakness(final_score)
    if category == "strength":
        save_strength(f"{role} __ {answer}")
    else:
        save_weakness(f"{role} __ {answer}")

    return{
        "score": final_score,
        "improvement": improvement,
        "brief_feedback": brief,
        "ai_feedback": ai_feedback
    }    