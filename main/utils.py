import os
import re
import tempfile
import fitz

from pytube import YouTube
from langchain.text_splitter import RecursiveCharacterTextSplitter
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import streamlit as st

import re
import logging
from typing import Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
    CouldNotRetrieveTranscript
)
import streamlit as st

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_video_id(url: str) -> Optional[str]:
    """Extract YouTube video ID from URL"""
    patterns = [
        r'(?:v=|youtu\.be\/)([\w-]{11})',
        r'youtube\.com\/watch\?.*v=([\w-]{11})',
        r'youtube\.com\/embed\/([\w-]{11})'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_youtube_transcript(url: str) -> str:
    """Fetch YouTube transcript or return error message"""
    try:
        video_id = extract_video_id(url)
        if not video_id:
            return "❌ Invalid YouTube URL"
        
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id,
            languages=['en', 'en-US', 'en-GB']
        )
        return " ".join([t['text'] for t in transcript])
        
    except NoTranscriptFound:
        return "❌ No English transcript available"
    except TranscriptsDisabled:
        return "❌ Transcripts are disabled for this video"
    except VideoUnavailable:
        return "❌ Video is private or unavailable"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def clean_text(text: str) -> str:
    """Clean and normalize text"""
    return re.sub(r'\s+', ' ', text.strip())

def split_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 100) -> list[str]:
    """Split text into chunks"""
    if not isinstance(text, str):
        raise ValueError("Input must be a string")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return text_splitter.split_text(clean_text(text))

def clean_text(text):
    return re.sub(r'\s+', ' ', text.strip())


def split_text(text, chunk_size=1000, chunk_overlap=100):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return text_splitter.split_text(clean_text(text))


def load_pdf(uploaded_file):
    try:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            text = "\n".join([page.get_text() for page in doc])
        return clean_text(text)
    except Exception as e:
        print(f"PDF load error: {e}")
        return None
