def keyword_match_score(answer, keywords):
    """
    Simple function to calculate a keyword match score for the answer.
    """
    answer = answer.lower()
    matched = sum(1 for kw in keywords if kw.lower() in answer)
    return matched 

def generate_score(keyword_score, difficulty = "medium"):
    """
    convert the keyword score into a final score out of 10.
    Difficulty slightly adjusts the scoring curve.
    """
    base = keyword_score * 2
    if difficulty == "hard":
        base -= 1
    elif difficulty == "easy":
         base -= 1
    
    return max(0, min(10, base))

def improvement_tips(keywords, answer):
    """
    returns which important keywords the user missed.
    """ 
    answer = answer.lower()
    missed_keywords = [kw for kw in keywords if kw.lower() not in answer]
    
    if not missed_keywords:
        return "Great job! You included all the important keywords."
    missing_list = ", ".join(missed_keywords)
    return f"You missed the following important keywords: {missing_list}. Try to include them in your answer for a better score!"

def classify_strength_or_weakness(score):
    """
    Basic rule to classify user's performance
    """
    if score >= 7:
        return "Strength"
    return "Weakness"

def short_feedback(score):
    """
    Simple qualitative feedback based on the score.
    """
    if score >= 6:
        return "Excellent! You're well-prepared for this question."
    elif score >= 4:
        return "Good effort! With a bit more practice, you'll be ready."
    else:
        return "Needs improvement. Focus on the key concepts and try again."