from interview_agent import generate_questions, analyze_answer
from memory_manager import save_interview_record, get_memory_summary

class InterviewRouter:
    def __init__(self, role, role_data):
        self.role = role
        self.role_data = role_data
        self.current_question = ""
        self.question_count=0
        self.max_questions=3
        self.waiting_for_answer=False


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

        save_interview_record(
            self.role,
            self.current_question,
            user_answer,
            feedback
        )

        return {
            "type": "analysis",
            "score": feedback["score"],
            "brief_feedback": feedback["brief_feedback"],
            "improvement_tips": feedback["improvement"],
            "ai_feedback": feedback["ai_analysis"]
        }
    
    def final_report(self):
        memory = get_memory_summary()
        return {
            "type": "final_report",
            "total_questions": self.question_count,
            "strengths": memory["strengths"][-5:],
            "weaknesses": memory["weaknesses"][-5:],
            "message": "Interview completed. Here is a summary of your performance based on the last 5 questions."
        }