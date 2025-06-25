from langchain.text_splitter import RecursiveCharacterTextSplitter
import fitz  # PyMuPDF

import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

def extract_youtube_transcript(url: str) -> str:
    # Extract video ID from the URL
    video_id_match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", url)
    if not video_id_match:
        raise ValueError("Invalid YouTube URL")
    video_id = video_id_match.group(1)

    try:
        # Fetch any available transcript (manual or auto, any language)
        transcript_obj = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_obj.find_transcript([t.language_code for t in transcript_obj])
        transcript_data = transcript.fetch()
        return TextFormatter().format_transcript(transcript_data)

    except Exception as e:
        print(f"❌ Raw error fetching transcript: {e}")
        raise RuntimeError(f"Failed to fetch transcript: {e}")


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
