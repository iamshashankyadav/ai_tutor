from youtube_transcript_api import YouTubeTranscriptApi
from langchain.text_splitter import RecursiveCharacterTextSplitter
import fitz  # PyMuPDF
import re

def extract_youtube_transcript(url):
    try:
        video_id = url.split("v=")[-1].split("&")[0]
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([t['text'] for t in transcript_list])
    except Exception as e:
        print(f"Transcript error: {e}")
        return None

def clean_text(text):
    return re.sub(r'\s+', ' ', text.strip())

def split_text(text, chunk_size=1000, chunk_overlap=100):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_text(clean_text(text))

def load_pdf(uploaded_file):
    try:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            text = "\n".join([page.get_text() for page in doc])
        return clean_text(text)
    except Exception as e:
        print(f"PDF load error: {e}")
        return None
