
🧠 AI Interview Assistant

An AI-powered interview preparation web app built with Streamlit that helps users practice interviews using resume-based questions and performance feedback.

🚀 Features
📄 Upload Resume (PDF)
🧠 Extract skills from resume
🎤 Generate interview questions
✍️ Answer practice section
📊 ATS-style score
💡 Feedback & improvement suggestions
🎨 Clean Streamlit UI
🛠️ Tech Stack
Python 🐍
Streamlit
PyPDF2
Pandas
Plotly
NLP (basic keyword extraction)
📁 Project Structure
AI-Interview-Assistant/
│
├── app.py
├── resume_parser.py
├── question_generator.py
├── feedback.py
├── requirements.txt
├── assets/
│   └── logo.jpg
⚙️ Installation & Run
git clone https://github.com/your-username/AI-Interview-Assistant.git
cd AI-Interview-Assistant
Create virtual environment
python3 -m venv venv
source venv/bin/activate
Install dependencies
pip install -r requirements.txt
Run app
streamlit run app.py
📦 requirements.txt
streamlit
PyPDF2
pandas
plotly
nltk
streamlit-option-menu
🧠 How It Works
User uploads resume
Text is extracted from PDF
Skills are detected using keywords
Interview questions are generated
User writes answers
System gives score + feedback
🔥 Future Improvements
GPT-powered smart interview bot
Voice-based interview system
Real-time answer evaluation
PDF report generation
Advanced ATS scoring system
👩‍💻 Author

Kainat Bashir
