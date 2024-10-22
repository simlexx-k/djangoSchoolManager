def get_grade(score):
    if not isinstance(score, (int, float)):
        raise ValueError("Score must be a number")
    
    if score >= 75:
        return 'EE'  # Exceeding Expectations
    elif score >= 50:
        return 'ME'  # Meeting Expectations
    elif score >= 25:
        return 'AE'  # Approaching Expectations
    else:
        return 'BE'  # Below Expectations

def get_auto_comment(score):
    if score >= 80:
        return "Excellent performance! Keep up the great work."
    elif 70 <= score < 80:
        return "Very good performance. You're on the right track."
    elif 60 <= score < 70:
        return "Good effort. With more practice, you can improve."
    elif 50 <= score < 60:
        return "Fair performance. Focus on areas needing improvement."
    else:
        return "Needs improvement. Let's work together to boost score."

