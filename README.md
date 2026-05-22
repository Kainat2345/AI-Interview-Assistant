
AI Interview Assistant 🤖

An AI-powered Interview Assistant built with Streamlit and OpenAI API. It can generate interview questions and evaluate user answers intelligently.

🚀 Features
Generate interview questions dynamically
Evaluate user answers using AI
Simple Streamlit UI
ATS-style scoring system (if implemented)
Secure API key handling using .env
🛠️ Tech Stack
Python
Streamlit
OpenAI API
python-dotenv
📁 Project Structure
AI-interview-assistant/
│── app.py
│── gpt_engine.py
│── .env
│── .gitignore
│── requirements.txt
│── venv/
⚙️ Setup Instructions
1. Clone the repository
git clone https://github.com/your-username/AI-interview-assistant.git
cd AI-interview-assistant
2. Create virtual environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
3. Install dependencies
pip install -r requirements.txt
4. Add API Key (IMPORTANT)

Create a .env file in the root folder:

OPENAI_API_KEY=your_api_key_here

⚠️ Never upload .env to GitHub.

▶️ Run the App
streamlit run app.py
🔐 Security Note
API keys are stored in .env file
.env is ignored using .gitignore
Never hardcode secrets in code
📌 Git Push Updates

To update existing GitHub repo:

git add .
git commit -m "Updated project with secure API handling"
git push origin main
💡 Future Improvements
Add speech-to-text interview mode
Add resume-based question generation
Deploy on Streamlit Cloud / Render
👨‍💻 Author

Developed as an AI learning project for interview preparation and practice.
