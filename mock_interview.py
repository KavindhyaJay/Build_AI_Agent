from roles import choose_role
from router import InterviewRouter

def run_interview():
    print("\n =========== AI INTERVIEW COACH ============\n - mock_interview.py:5")

    role, role_data = choose_role()

    router = InterviewRouter(role, role_data)

    print("\n Starting interview.... \n - mock_interview.py:11")

    while True:
        step = router.next_step()

        if step["type"] == "question":
            # Check if the generated text is actually an error
            if step["text"].startswith("Error:"):
                print(f"\n[!] API Error: {step['text']} - mock_interview.py:19")
                print("Exiting interview. Please wait a moment and try again. - mock_interview.py:20")
                break # Break the loop instead of asking for an answer

            print(f"\nQuestion {router.question_count}: {step['text']} - mock_interview.py:23")
            answer = input("Your Answer: ")
            
            analysis = router.next_step(answer)

            print("\n ====== FEEDBACK: ====== \n - mock_interview.py:28")
            print(f"Score: {analysis['score']}/10 - mock_interview.py:29")
            print(f"Quick Feedback: {analysis['brief_feedback']} - mock_interview.py:30")
            print(f"Missing Points: {analysis['improvement_tips']} - mock_interview.py:31")
            print(f"\n AI Feedback: - mock_interview.py:32")
            print(f"{analysis['ai_feedback']} - mock_interview.py:33")

        elif step["type"] == "final_report":
            print("\n ====== FINAL INTERVIEW REPORT: ====== \n - mock_interview.py:36")
            print(f"Total Questions Answered: {step['total_questions']} - mock_interview.py:37")
            print(f"\nYour Strengths: - mock_interview.py:38")
            if step["strengths"]:
                for s in step["strengths"]:
                    print(f"✓ {s} - mock_interview.py:41")

            else:
                print("No clear strengths identified. Focus on improving your answers based on the feedback provided. - mock_interview.py:44")

            print(f"\nAreas to Improvement: - mock_interview.py:46")    
            if step["weaknesses"]:
                for w in step["weaknesses"]:
                    print(f"✗ {w} - mock_interview.py:49")
            else:
                print("No clear weaknesses identified. Great job! Keep practicing to maintain your strengths. - mock_interview.py:51")

            print(f"\n{step['message']} - mock_interview.py:53")
            print("\n===================================================\n - mock_interview.py:54")
            break
if __name__ == "__main__":
    run_interview()