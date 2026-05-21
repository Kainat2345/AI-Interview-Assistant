def generate_questions(skills):

    questions = []

    if "python" in skills.lower():
        questions.append("Explain OOP concepts in Python.")

    if "machine learning" in skills.lower():
        questions.append("Difference between supervised and unsupervised learning?")

    if "sql" in skills.lower():
        questions.append("What is JOIN in SQL?")

    questions.extend([
        "Tell me about yourself.",
        "Why should we hire you?",
        "Describe one challenging project."
    ])

    return questions