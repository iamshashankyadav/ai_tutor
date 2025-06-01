from fastapi import FastAPI, APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
import io
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime
import fitz  # PyMuPDF
import chromadb
from sentence_transformers import SentenceTransformer
from youtube_transcript_api import YouTubeTranscriptApi
import re
import asyncio
from urllib.parse import urlparse, parse_qs


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Initialize AI components
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
chroma_client = chromadb.Client()

# Try to get existing collection or create new one
try:
    knowledge_collection = chroma_client.get_collection("knowledge_base")
except:
    knowledge_collection = chroma_client.create_collection("knowledge_base")

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Models
class QuestionRequest(BaseModel):
    question: str
    difficulty: Optional[str] = "intermediate"  # beginner, intermediate, advanced

class YouTubeRequest(BaseModel):
    youtube_url: str
    difficulty: Optional[str] = "intermediate"

class AnswerResponse(BaseModel):
    answer: str
    explanation: str
    sources: List[str]
    confidence: float
    difficulty: str

class DocumentInfo(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    content_type: str  # pdf, youtube, text
    upload_time: datetime = Field(default_factory=datetime.utcnow)
    chunks_count: int

# Utility functions
def chunk_text(text: str, chunk_size: int = 512, overlap: int = 50) -> List[str]:
    """Split text into overlapping chunks"""
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk.strip())
    
    return chunks

def extract_pdf_text(pdf_file: bytes) -> str:
    """Extract text from PDF file"""
    try:
        pdf_document = fitz.open(stream=pdf_file, filetype="pdf")
        text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text += page.get_text()
        pdf_document.close()
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing PDF: {str(e)}")

def extract_youtube_id(url: str) -> str:
    """Extract YouTube video ID from URL"""
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed\/)([0-9A-Za-z_-]{11})',
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    raise HTTPException(status_code=400, detail="Invalid YouTube URL")

async def get_youtube_transcript(video_id: str) -> str:
    """Get transcript from YouTube video"""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = ' '.join([entry['text'] for entry in transcript])
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error getting YouTube transcript: {str(e)}")

def store_document_chunks(doc_id: str, chunks: List[str], metadata: Dict[str, Any]):
    """Store document chunks in ChromaDB"""
    try:
        embeddings = embedding_model.encode(chunks)
        
        ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [{"doc_id": doc_id, "chunk_index": i, **metadata} for i in range(len(chunks))]
        
        knowledge_collection.add(
            embeddings=embeddings.tolist(),
            documents=chunks,
            metadatas=metadatas,
            ids=ids
        )
        return True
    except Exception as e:
        logging.error(f"Error storing chunks: {str(e)}")
        return False

def search_knowledge_base(query: str, n_results: int = 5) -> Dict[str, Any]:
    """Search knowledge base for relevant chunks"""
    try:
        query_embedding = embedding_model.encode([query])
        results = knowledge_collection.query(
            query_embeddings=query_embedding.tolist(),
            n_results=n_results
        )
        return results
    except Exception as e:
        logging.error(f"Error searching knowledge base: {str(e)}")
        return {"documents": [[]], "metadatas": [[]], "distances": [[]]}

def generate_answer_with_context(question: str, context_chunks: List[str], difficulty: str = "intermediate") -> Dict[str, Any]:
    """Generate answer using context (placeholder for now - will use actual LLM later)"""
    # For now, return a structured response based on context
    if not context_chunks:
        return {
            "answer": "I don't have enough information to answer this question. Please upload relevant documents or provide more context.",
            "explanation": "No relevant context found in the knowledge base.",
            "confidence": 0.1
        }
    
    # Simple contextual response (in real implementation, this would use LLM)
    context_text = "\n".join(context_chunks[:3])  # Use top 3 chunks
    
    # Difficulty-based response
    if difficulty == "beginner":
        explanation_style = "This is a basic explanation: "
    elif difficulty == "advanced":
        explanation_style = "This is an advanced analysis: "
    else:
        explanation_style = "Here's an intermediate explanation: "
    
    answer = f"Based on the provided context, {question.lower()}"
    explanation = f"{explanation_style}The relevant information suggests that " + context_text[:200] + "..."
    
    return {
        "answer": answer,
        "explanation": explanation,
        "confidence": 0.8 if len(context_chunks) >= 3 else 0.6
    }

# API Endpoints
@api_router.get("/")
async def root():
    return {"message": "AI Tutor Backend - Ready to help Indian students learn!"}

@api_router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload and process PDF document"""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        # Read PDF content
        pdf_content = await file.read()
        text = extract_pdf_text(pdf_content)
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="No text found in PDF")
        
        # Create document info
        doc_id = str(uuid.uuid4())
        doc_info = DocumentInfo(
            id=doc_id,
            title=file.filename,
            content_type="pdf",
            chunks_count=0
        )
        
        # Chunk the text
        chunks = chunk_text(text)
        doc_info.chunks_count = len(chunks)
        
        # Store in vector database
        metadata = {
            "title": file.filename,
            "content_type": "pdf"
        }
        
        success = store_document_chunks(doc_id, chunks, metadata)
        if not success:
            raise HTTPException(status_code=500, detail="Error storing document")
        
        # Store document info in MongoDB
        await db.documents.insert_one(doc_info.dict())
        
        return {
            "message": "PDF uploaded and processed successfully",
            "document_id": doc_id,
            "chunks_processed": len(chunks),
            "title": file.filename
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

@api_router.post("/upload-youtube")
async def upload_youtube(request: YouTubeRequest):
    """Process YouTube video transcript"""
    try:
        # Extract video ID
        video_id = extract_youtube_id(request.youtube_url)
        
        # Get transcript
        transcript_text = await get_youtube_transcript(video_id)
        
        if not transcript_text.strip():
            raise HTTPException(status_code=400, detail="No transcript found for this video")
        
        # Create document info
        doc_id = str(uuid.uuid4())
        doc_info = DocumentInfo(
            id=doc_id,
            title=f"YouTube Video: {video_id}",
            content_type="youtube",
            chunks_count=0
        )
        
        # Chunk the transcript
        chunks = chunk_text(transcript_text)
        doc_info.chunks_count = len(chunks)
        
        # Store in vector database
        metadata = {
            "title": f"YouTube Video: {video_id}",
            "content_type": "youtube",
            "video_id": video_id,
            "url": request.youtube_url
        }
        
        success = store_document_chunks(doc_id, chunks, metadata)
        if not success:
            raise HTTPException(status_code=500, detail="Error storing transcript")
        
        # Store document info in MongoDB
        await db.documents.insert_one(doc_info.dict())
        
        return {
            "message": "YouTube transcript processed successfully",
            "document_id": doc_id,
            "chunks_processed": len(chunks),
            "video_id": video_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing YouTube video: {str(e)}")

@api_router.post("/ask-question", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """Answer question using RAG"""
    try:
        # Search knowledge base
        search_results = search_knowledge_base(request.question)
        
        context_chunks = []
        sources = []
        
        if search_results["documents"] and search_results["documents"][0]:
            context_chunks = search_results["documents"][0]
            
            # Extract sources from metadata
            for metadata in search_results["metadatas"][0]:
                if metadata:
                    source = metadata.get("title", "Unknown source")
                    if source not in sources:
                        sources.append(source)
        
        # Generate answer
        answer_data = generate_answer_with_context(
            request.question, 
            context_chunks, 
            request.difficulty
        )
        
        return AnswerResponse(
            answer=answer_data["answer"],
            explanation=answer_data["explanation"],
            sources=sources,
            confidence=answer_data["confidence"],
            difficulty=request.difficulty
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating answer: {str(e)}")

@api_router.get("/documents")
async def get_documents():
    """Get list of uploaded documents"""
    try:
        # Exclude MongoDB's _id field to avoid ObjectId serialization issues
        documents = await db.documents.find({}, {"_id": 0}).sort("upload_time", -1).to_list(100)
        return {"documents": documents}
    except Exception as e:
        logger.error(f"Error retrieving documents: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving documents: {str(e)}")

@api_router.post("/generate-flashcards/{document_id}")
async def generate_flashcards(document_id: str):
    """Generate Q&A flashcards from document"""
    try:
        # Get document chunks from ChromaDB
        results = knowledge_collection.get(
            where={"doc_id": document_id},
            include=["documents", "metadatas"]
        )
        
        if not results["documents"]:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Generate simple flashcards (in real implementation, use LLM)
        flashcards = []
        for i, chunk in enumerate(results["documents"][:5]):  # Limit to 5 flashcards
            question = f"What is the main concept discussed in section {i+1}?"
            answer = chunk[:200] + "..." if len(chunk) > 200 else chunk
            
            flashcards.append({
                "question": question,
                "answer": answer,
                "chunk_index": i
            })
        
        return {"flashcards": flashcards}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating flashcards: {str(e)}")

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
