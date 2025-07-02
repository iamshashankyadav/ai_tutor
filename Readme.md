# 🧠 AI Tutor – Personalized Learning Assistant for Indian Students

An intelligent, multilingual AI tutor that helps students learn by summarizing, questioning, and interacting with content from PDFs, YouTube videos, or custom text. Built to make quality education accessible for every Indian learner.

![AI Tutor](demo_images/Screenshot%202025-07-02%20141046.png) <!-- Replace with actual image -->
![AI Tutor](demo_images/Screenshot%202025-07-02%20141121.png) <!-- Replace with actual image -->
![AI Tutor](demo_images/Screenshot%202025-07-02%20141221.png) <!-- Replace with actual image -->
![AI Tutor](demo_images/Screenshot%202025-07-02%20141408.png) <!-- Replace with actual image -->
---

## 🚀 Features

- 📄 **PDF Upload** – Extracts and summarizes lecture notes or textbooks
- 🎥 **YouTube URL Support** – Pulls transcripts and generates summaries + Q&A
- ❓ **Ask Any Question** – Custom Q&A from your pasted content
- 🔗 **LLM-powered** – Uses LangChain + Groq for fast, intelligent answers
- 🧠 **Auto Q&A Generation** – Creates revision-style questions and answers
- 🌐 **Streamlit App** – Fully interactive frontend with instant feedback

---

## 🧪 Use Cases

- Quickly understand lengthy lecture slides or PDFs
- Summarize YouTube educational videos in seconds
- Generate revision material for competitive exams
- Practice answering key questions from class content

---

## 🛠️ Tech Stack

| Component        | Tool/Library                          |
|------------------|----------------------------------------|
| LLM Engine        | [Groq API](https://console.groq.com) via LangChain |
| Vector DB         | FAISS (in-memory)                     |
| PDF Processing    | PyMuPDF (`fitz`)                      |
| Video Processing  | youtube-transcript-api, pytube        |
| Frontend          | Streamlit                             |
| Language Handling | tiktoken, langchain-core              |

---

## ⚙️ Setup Instructions

```bash
# Clone the repo
git clone https://github.com/your-username/ai-tutor
cd ai-tutor

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
