import re
import logging
from typing import Optional, Tuple
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
    """Extract YouTube video ID from various URL formats"""
    patterns = [
        r'(?:v=|youtu\.be\/)([\w-]{11})',
        r'youtube\.com\/watch\?.*v=([\w-]{11})',
        r'youtube\.com\/embed\/([\w-]{11})',
        r'youtube\.com\/shorts\/([\w-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    st.error("❌ Invalid YouTube URL format")
    return None

def get_youtube_transcript(url: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Fetch YouTube transcript with proper error handling
    Returns tuple: (transcript_text, error_message)
    """
    try:
        video_id = extract_video_id(url)
        if not video_id:
            return None, "Invalid YouTube URL"
        
        logger.info(f"Fetching transcript for video ID: {video_id}")
        
        # Try multiple language fallbacks
        for lang in ['en', 'en-US', 'en-GB', None]:  # None = any language
            try:
                transcript = YouTubeTranscriptApi.get_transcript(
                    video_id,
                    languages=[lang] if lang else None
                )
                
                # Properly format the transcript segments
                transcript_text = " ".join([segment['text'] for segment in transcript])
                return transcript_text, None
                
            except (NoTranscriptFound, TranscriptsDisabled):
                continue
                
        return None, "No suitable transcript found"
        
    except VideoUnavailable:
        return None, "Video is private or unavailable"
    except CouldNotRetrieveTranscript:
        return None, "YouTube API returned empty data"
    except Exception as e:
        logger.error(f"Unexpected error: {type(e).__name__} - {str(e)}")
        return None, f"Unexpected error: {str(e)}"

# Test function
def test_transcript_extraction():
    test_urls = [
        "https://www.youtube.com/watch?v=jNQXAC9IVRw",  # Should work
        "https://youtu.be/dQw4w9WgXcQ",  # No transcript
        "invalid_url"  # Should fail
    ]
    
    for url in test_urls:
        print(f"\nTesting URL: {url}")
        transcript, error = get_youtube_transcript(url)
        if transcript:
            print(f"Success! First 50 chars: {transcript[:50]}...")
        else:
            print(f"Failed: {error}")

if __name__ == "__main__":
    test_transcript_extraction()