import os
import requests
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
import re

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def call_groq_mixtral(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mixtral-8x7b-32768",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3
    }
    response = requests.post(GROQ_URL, json=data, headers=headers)
    return response.json()["choices"][0]["message"]["content"]

def generate_answer_with_sources(question, chunks):
    context = "\n".join(chunks)
    prompt = f"""
Answer the question using only the context below. Return answer and the exact line(s) you used.

Context:
{context}

Question:
{question}

Return in format:
Answer: <your answer>
Sources:
- <line 1>
- <line 2>
"""
    response = call_groq_mixtral(prompt)
    answer = response.split("Sources:")[0].replace("Answer:", "").strip()
    sources = response.split("Sources:")[-1].strip().split("- ")
    sources = [s.strip() for s in sources if s.strip()]
    return answer, sources

def summarize_text(chunks):
    context = "\n".join(chunks[:20])  # truncate if too long
    prompt = f"""
Summarize the following content clearly for a student:

{context}

Summary:
"""
    return call_groq_mixtral(prompt).strip()

def generate_qna(chunks, num=5):
    context = "\n".join(chunks[:20])
    prompt = f"""
Generate {num} question-answer pairs to help a student revise the material below:

{context}

Return as:
Q: <question>
A: <answer>
...repeat
"""
    output = call_groq_mixtral(prompt)
    qa_pairs = re.findall(r"Q:(.*?)A:(.*?)\n", output, re.DOTALL)
    return [(q.strip(), a.strip()) for q, a in qa_pairs if q.strip() and a.strip()]
