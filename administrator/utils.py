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
