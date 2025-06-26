import streamlit as st
from utils import get_youtube_transcript, split_text, load_pdf
from chains import generate_answer_with_sources, summarize_text, generate_qna
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="AI Tutor for Every Indian Student", layout="wide")
st.title("📚 AI Tutor")

input_mode = st.radio("Select input type:", ["Upload PDF", "YouTube URL", "Ask a Question"], horizontal=True)

chunks = []

if input_mode == "Upload PDF":
    uploaded_file = st.file_uploader("Upload a PDF file:", type=["pdf"])
    if uploaded_file is not None:
        pdf_text = load_pdf(uploaded_file)
        if pdf_text:
            chunks = split_text(pdf_text)
            st.success(f"✅ PDF loaded and split into {len(chunks)} chunks.")
            with st.expander("Summarize PDF"):
                if st.button("Summarize PDF"):
                    summary = summarize_text(chunks)
                    st.info(summary)

            with st.expander("Generate Q&A"):
                if st.button("Generate Q&A"):
                    qna_list = generate_qna(chunks)
                    for q, a in qna_list:
                        st.markdown(f"**Q:** {q}\n\n**A:** {a}\n")
        else:
            st.error("❌ Could not extract text from PDF.")

elif input_mode == "YouTube URL":
    yt_url = st.text_input("Enter YouTube video URL:")
    if yt_url:
        transcript = get_youtube_transcript(yt_url)
        # print(transcript)
        if transcript:
            chunks = split_text(transcript)
            st.success(f"✅ Transcript loaded and split into {len(chunks)} chunks.")

            with st.expander("Summarize Video"):
                if st.button("Summarize Video"):
                    summary = summarize_text(chunks)
                    st.info(summary)

            with st.expander("Generate Q&A"):
                if st.button("Generate Q&A"):
                    qna_list = generate_qna(chunks)
                    for q, a in qna_list:
                        st.markdown(f"**Q:** {q}\n\n**A:** {a}\n")
        else:
            st.error("❌ Could not fetch transcript.")

elif input_mode == "Ask a Question":
    user_question = st.text_input("Ask your question:")
    text_context = st.text_area("Paste related text (PDF content or transcript):", height=200)
    if st.button("Get Answer"):
        if user_question and text_context:
            chunks = split_text(text_context)
            answer, sources = generate_answer_with_sources(user_question, chunks)
            st.markdown(f"**Answer:** {answer}")
            st.markdown("**Source Line(s):**")
            for line in sources:
                st.code(line)
        else:
            st.warning("⚠️ Please provide both a question and supporting content.")
