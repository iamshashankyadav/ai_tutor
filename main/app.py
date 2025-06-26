import streamlit as st
from utils import get_youtube_transcript, split_text, load_pdf
from chains import generate_answer_with_sources, summarize_text, generate_qna
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# ========== Dark Mode UI Configuration ==========
st.set_page_config(
    page_title="AI Tutor for Every Indian Student",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark mode CSS
st.markdown("""
    <style>
        :root {
            --primary: #2b313e;
            --secondary: #3b4252;
            --accent: #81a1c1;
            --text: #e5e9f0;
            --success: #a3be8c;
            --error: #bf616a;
        }
        
        body {
            color: var(--text);
            background-color: var(--primary);
        }
        
        .main {
            background-color: var(--primary);
        }
        
        .stRadio > div {
            display: flex;
            justify-content: center;
            gap: 20px;
        }
        
        .stButton>button {
            background-color: var(--accent);
            color: var(--primary);
            border-radius: 5px;
            padding: 0.5rem 1rem;
            font-weight: 500;
            width: 100%;
            border: none;
        }
        
        .stButton>button:hover {
            background-color: #88c0d0;
        }
        
        .stTextInput>div>div>input, 
        .stTextArea>div>div>textarea {
            background-color: var(--secondary);
            color: var(--text);
            border-radius: 5px;
            border: 1px solid var(--accent);
        }
        
        .stExpander {
            background-color: var(--secondary);
            border-radius: 5px;
            border: 1px solid var(--accent);
        }
        
        .stAlert {
            background-color: var(--secondary);
            border-radius: 5px;
        }
        
        .success-box {
            background-color: #2e3440;
            padding: 1rem;
            border-radius: 5px;
            border-left: 4px solid var(--success);
            color: var(--text);
        }
        
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: var(--accent);
        }
        
        .sidebar .sidebar-content {
            background-color: var(--secondary) !important;
        }
        
        hr {
            border-color: var(--accent);
        }
    </style>
""", unsafe_allow_html=True)

# ========== Main App ==========
st.title("📚 AI Tutor - Smart Learning Companion")
st.markdown("---")

# Dark mode sidebar
with st.sidebar:
    st.header("About")
    st.markdown("""
    <style>
        .sidebar .markdown-text-container {
            color: var(--text);
        }
    </style>
    
    This AI Tutor helps you:
    - 📝 Summarize PDFs
    - ▶️ Understand YouTube videos
    - ❓ Answer questions from content
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("Made with ❤️ for Indian students")

# Input selection
input_mode = st.radio(
    "Select input type:",
    ["Upload PDF", "YouTube URL", "Ask a Question"],
    horizontal=True,
    key="input_selector"
)

st.markdown("---")

chunks = []

if input_mode == "Upload PDF":
    st.subheader("📄 PDF Processor")
    uploaded_file = st.file_uploader(
        "Upload your PDF file:",
        type=["pdf"],
        help="Upload lecture notes, textbooks or study materials"
    )
    
    if uploaded_file is not None:
        with st.spinner("Processing PDF..."):
            pdf_text = load_pdf(uploaded_file)
            if pdf_text:
                chunks = split_text(pdf_text)
                st.markdown(f"""
                <div class="success-box">
                    ✅ PDF loaded successfully! Split into <strong>{len(chunks)}</strong> chunks.
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    with st.expander("📝 Summarize PDF", expanded=False):
                        if st.button("Generate Summary"):
                            with st.spinner("Generating summary..."):
                                summary = summarize_text(chunks)
                                st.info(summary)
                
                with col2:
                    with st.expander("❓ Generate Q&A", expanded=False):
                        if st.button("Generate Questions"):
                            with st.spinner("Creating Q&A pairs..."):
                                qna_list = generate_qna(chunks)
                                for i, (q, a) in enumerate(qna_list, 1):
                                    st.markdown(f"""
                                    <div style="margin-bottom: 1rem; color: var(--text);">
                                        <h4 style="color: var(--accent);">Q{i}: {q}</h4>
                                        <p>{a}</p>
                                    </div>
                                    """, unsafe_allow_html=True)
            else:
                st.error("❌ Could not extract text from PDF. Please try a different file.")

elif input_mode == "YouTube URL":
    st.subheader("▶️ YouTube Video Processor")
    yt_url = st.text_input(
        "Enter YouTube video URL:",
        placeholder="https://www.youtube.com/watch?v=...",
        help="Paste a link to any educational YouTube video"
    )
    
    if yt_url:
        with st.spinner("Fetching transcript..."):
            transcript = get_youtube_transcript(yt_url)
            
            if transcript and not transcript.startswith("❌"):
                chunks = split_text(transcript)
                st.markdown(f"""
                <div class="success-box">
                    ✅ Transcript loaded successfully! Split into <strong>{len(chunks)}</strong> chunks.
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    with st.expander("📝 Summarize Video", expanded=False):
                        if st.button("Generate Summary"):
                            with st.spinner("Generating summary..."):
                                summary = summarize_text(chunks)
                                st.info(summary)
                
                with col2:
                    with st.expander("❓ Generate Q&A", expanded=False):
                        if st.button("Generate Questions"):
                            with st.spinner("Creating Q&A pairs..."):
                                qna_list = generate_qna(chunks)
                                for i, (q, a) in enumerate(qna_list, 1):
                                    st.markdown(f"""
                                    <div style="margin-bottom: 1rem; color: var(--text);">
                                        <h4 style="color: var(--accent);">Q{i}: {q}</h4>
                                        <p>{a}</p>
                                    </div>
                                    """, unsafe_allow_html=True)
            else:
                st.error(transcript or "❌ Could not fetch transcript. Try a different video.")

elif input_mode == "Ask a Question":
    st.subheader("❓ Question Answering")
    col1, col2 = st.columns([3, 2])
    
    with col1:
        user_question = st.text_input(
            "Enter your question:",
            placeholder="What is the main idea of this text?",
            help="Ask anything about the provided content"
        )
        
    with col2:
        text_context = st.text_area(
            "Paste related text (PDF content or transcript):",
            height=200,
            help="Copy-paste text from your materials or generated transcripts"
        )
    
    if st.button("Get Answer", key="answer_btn"):
        if user_question and text_context:
            with st.spinner("Analyzing content..."):
                chunks = split_text(text_context)
                answer, sources = generate_answer_with_sources(user_question, chunks)
                
                st.markdown("---")
                st.markdown(f"""
                <div style="background-color: #3b4252; padding: 1rem; border-radius: 5px; color: var(--text);">
                    <h3 style="color: var(--accent);">Answer:</h3>
                    <p>{answer}</p>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("🔍 View Sources", expanded=False):
                    st.markdown("**Relevant content used:**")
                    for i, line in enumerate(sources, 1):
                        st.markdown(f"{i}. `{line}`", unsafe_allow_html=True)
        else:
            st.warning("⚠️ Please provide both a question and supporting content")

# Footer
st.markdown("---")
st.caption("AI Tutor v1.0 | Made for Indian Students")