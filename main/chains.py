from dotenv import load_dotenv
import os
import re
from langchain_groq import ChatGroq

from langchain.schema import HumanMessage

load_dotenv()

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

def call_groq_llama(prompt):
    try:
        response = llm([HumanMessage(content=prompt)])
        return response.content.strip()
    except Exception as e:
        print("❌ LangChain Groq LLaMA error:", e)
        return "LLM call failed."



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
    response = call_groq_llama(prompt)
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
    return call_groq_llama(prompt)


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
    output = call_groq_llama(prompt)
    qa_pairs = re.findall(r"Q:(.*?)A:(.*?)\n", output, re.DOTALL)
    return [(q.strip(), a.strip()) for q, a in qa_pairs if q.strip() and a.strip()]
