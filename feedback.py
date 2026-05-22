def calculate_ats_score(resume_text, skills):
    resume_text = resume_text.lower()

    keyword_weight = {
        "python": 20,
        "machine learning": 25,
        "sql": 15,
        "deep learning": 25,
        "data science": 15
    }

    score = 0

    for skill, weight in keyword_weight.items():
        if skill in resume_text:
            score += weight

    return min(score, 100)


def get_feedback(score):
    if score >= 80:
        return "Excellent Resume 🔥"
    elif score >= 50:
        return "Good Resume 👍"
    else:
        return "Needs Improvement ⚠️"