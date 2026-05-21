def generate_feedback(answer):

    if len(answer) < 50:
        return "Answer is too short. Add more explanation."

    elif len(answer) < 150:
        return "Good answer but can be improved with examples."

    else:
        return "Excellent detailed answer!"