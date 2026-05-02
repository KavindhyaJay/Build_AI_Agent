from interview_agent import generate_questions, analyze_answer
from memory_manager import save_interview_record, get_memory_summary, save_strength, save_weakness

class InterviewRouter:
    def __init__(self, role, role_data):
        self.role = role
        self.role_data = role_data
        self.current_question = ""
        self.question_count = 0
        self.max_questions = 3
        self.waiting_for_answer = False

    def next_step(self, user_input=None):
        if self.question_count == 0:
            return self.ask_new_question()
        if self.waiting_for_answer and user_input:
            return self.process_answer(user_input)
        
        if self.question_count < self.max_questions:
            return self.ask_new_question()
        return self.final_report()
    
    def ask_new_question(self):
        self.current_question = generate_questions(self.role)
        self.question_count += 1
        self.waiting_for_answer = True
        return {
            "type": "question",
            "text": self.current_question
        }
    
    def process_answer(self, user_answer):
        self.waiting_for_answer = False

        feedback = analyze_answer(self.role, user_answer, self.role_data)
        
        # --- NEW LOGIC: Save to Strengths & Weaknesses ---
        score = feedback.get("score", 0)
        if score >= 7:
            # If you did well, save the brief feedback as a strength
            save_strength(feedback.get("brief_feedback", "Strong technical response."))
        else:
            # If you scored low, save the improvement tips as a weakness
            save_weakness(feedback.get("improvement_tips", "Needs review of core concepts."))

        save_interview_record(
            self.role,
            self.current_question,
            user_answer,
            feedback
        )

        return {
            "type": "analysis",
            "score": score,
            "brief_feedback": feedback.get("brief_feedback", ""),
            "improvement_tips": feedback.get("improvement_tips", ""),
            "ai_feedback": feedback.get("ai_feedback", "")
        }
    
    def final_report(self):
        memory = get_memory_summary() or {"strengths": [], "weaknesses": []}
        return {
            "type": "final_report",
            "total_questions": self.question_count,
            "strengths": memory["strengths"][-5:], # Gets the last 5 strengths
            "weaknesses": memory["weaknesses"][-5:], # Gets the last 5 weaknesses
            "message": "Interview completed. Here is a summary of your performance based on the last 5 questions."
        }