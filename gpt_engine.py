import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found")

client = genai.Client(api_key=api_key)

MODEL = "gemini-2.5-flash"


def generate_questions(prompt):
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )
    return response.text


def evaluate_answer(question, answer):
    prompt = f"""
Question: {question}
Answer: {answer}
Give score out of 10 with feedback.
"""
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )
    return response.text