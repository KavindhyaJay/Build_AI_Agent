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
            print(f"\nQuestion {router.question_count}: {step['text']}\n - mock_interview.py:17")
            answer = input("Your Answer: ")
            
            analysis = router.next_step(answer)

            print("\n ====== FEEDBACK: ====== \n - mock_interview.py:22")
            print(f"Score: {analysis['score']}/10 - mock_interview.py:23")
            print(f"Quick Feedback: {analysis['brief_feedback']} - mock_interview.py:24")
            print(f"Missing Points: {analysis['improvements']} - mock_interview.py:25")
            print(f"\n AI Feedback: - mock_interview.py:26")
            print(analysis["ai_feedback - mock_interview.py:27"])

        elif step["type"] == "final_report":
            print("\n ====== FINAL INTERVIEW REPORT: ====== \n - mock_interview.py:30")
            print(f"Total Questions Answered: {step['total_questions']} - mock_interview.py:31")
            print(f"\nYour Strengths: - mock_interview.py:32")
            if step["strengths"]:
                for s in step["strengths"]:
                    print(f"✓ {s} - mock_interview.py:35")

            else:
                print("No clear strengths identified. Focus on improving your answers based on the feedback provided. - mock_interview.py:38")

            print(f"\nAreas to Improvement: - mock_interview.py:40")    
            if step["weaknesses"]:
                for w in step["weaknesses"]:
                    print(f"✗ {w} - mock_interview.py:43")
            else:
                print("No clear weaknesses identified. Great job! Keep practicing to maintain your strengths. - mock_interview.py:45")

            print(f"\n{step['message']} - mock_interview.py:47")
            print("\n===================================================\n - mock_interview.py:48")
            break
if __name__ == "__main__":
    run_interview()