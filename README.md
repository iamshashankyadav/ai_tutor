# 🧠 AI Tutor for Every Indian Student

A comprehensive full-stack web application that provides personalized, multilingual, and explainable learning support to Indian students studying complex technical subjects.

## 🌟 Features

### Core Functionality
- **📄 PDF Processing**: Upload textbooks, notes, or any PDF for AI-powered learning assistance
- **📺 YouTube Integration**: Extract and process educational content from YouTube videos
- **❓ Intelligent Q&A**: Ask questions and get context-aware answers with explanations
- **🃏 Flashcard Generation**: Auto-generate study flashcards from uploaded content
- **📚 Document Management**: Track and manage all uploaded learning materials
- **🎯 Difficulty Levels**: Choose between Beginner, Intermediate, and Advanced explanations

### AI-Powered Features
- **RAG (Retrieval-Augmented Generation)**: Advanced question answering using context from uploaded documents
- **Semantic Search**: Find relevant information using AI embeddings
- **Content Chunking**: Intelligent text processing for optimal learning
- **Source Attribution**: Always know where answers come from
- **Confidence Scoring**: Get reliability metrics for AI responses

### Technical Excellence
- **Modern UI**: Beautiful, responsive design with Tailwind CSS
- **Real-time Processing**: Fast PDF and video transcript extraction
- **Vector Database**: ChromaDB for efficient semantic search
- **MongoDB**: Reliable document metadata storage
- **RESTful API**: Clean, well-documented backend architecture

## 🚀 Technology Stack

### Backend
- **FastAPI**: Modern, high-performance Python web framework
- **MongoDB**: Document database for metadata storage
- **ChromaDB**: Vector database for embeddings and semantic search
- **Sentence Transformers**: State-of-the-art text embeddings
- **PyMuPDF**: PDF text extraction
- **YouTube Transcript API**: Video content processing

### Frontend
- **React**: Modern JavaScript framework
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client for API communication
- **Responsive Design**: Works on desktop and mobile

### AI/ML Components
- **sentence-transformers/all-MiniLM-L6-v2**: Lightweight embedding model
- **Text Chunking**: Intelligent content segmentation
- **Vector Similarity Search**: Semantic content retrieval
- **Context-Aware Generation**: Smart response generation

## 📁 Project Structure

```
/app/
├── backend/                    # FastAPI backend
│   ├── server.py              # Main application file
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Environment variables
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── App.js             # Main React component
│   │   ├── App.css            # Component styles
│   │   ├── index.js           # Entry point
│   │   └── index.css          # Global styles
│   ├── package.json           # Node.js dependencies
│   ├── tailwind.config.js     # Tailwind configuration
│   ├── postcss.config.js      # PostCSS configuration
│   └── .env                   # Environment variables
├── backend_test.py            # API testing script
└── README.md                  # This file
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- MongoDB instance
- Git

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

### Frontend Setup
```bash
cd frontend
yarn install
```

### Environment Variables

**Backend (.env)**
```
MONGO_URL=mongodb://localhost:27017
DB_NAME=ai_tutor_db
```

**Frontend (.env)**
```
REACT_APP_BACKEND_URL=http://localhost:8001
```

## 🚀 Running the Application

### Start Backend
```bash
cd backend
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

### Start Frontend
```bash
cd frontend
yarn start
```

Access the application at `http://localhost:3000`

## 📖 API Documentation

### Core Endpoints

#### PDF Upload
```http
POST /api/upload-pdf
Content-Type: multipart/form-data

{
  "file": PDF_FILE
}
```

#### YouTube Processing
```http
POST /api/upload-youtube
Content-Type: application/json

{
  "youtube_url": "https://youtube.com/watch?v=...",
  "difficulty": "intermediate"
}
```

#### Ask Question
```http
POST /api/ask-question
Content-Type: application/json

{
  "question": "What is machine learning?",
  "difficulty": "beginner"
}
```

#### Get Documents
```http
GET /api/documents
```

#### Generate Flashcards
```http
POST /api/generate-flashcards/{document_id}
```

## 🎯 Usage Guide

### 1. Upload Learning Materials
- **PDF Upload**: Click "📄 PDF Upload" tab and select your textbook or notes
- **YouTube Processing**: Click "📺 YouTube" tab and paste an educational video URL

### 2. Ask Questions
- Go to "❓ Ask Question" tab
- Type your question about the uploaded content
- Select difficulty level (Beginner/Intermediate/Advanced)
- Get detailed answers with explanations and sources

### 3. Study with Flashcards
- View uploaded documents in "📚 Documents" tab
- Click "🃏 Generate Flashcards" for any document
- Study with interactive flashcards in "🃏 Flashcards" tab

### 4. Manage Content
- Track all uploaded materials in "📚 Documents" tab
- See processing statistics (chunks, upload time)
- Generate flashcards from any document

## 🧪 Testing

Run the comprehensive test suite:
```bash
python backend_test.py
```

The test script will:
- Test all API endpoints
- Create sample PDFs for testing
- Verify document processing
- Test question answering
- Validate flashcard generation

## 🔮 Future Enhancements

### Ready for Integration
- **LLM APIs**: Easy integration with OpenAI GPT-4, Anthropic Claude, or local models
- **Translation**: Google Translate API or AI4Bharat IndicTrans for Indian languages
- **Diagram Generation**: Mermaid.js for visual explanations
- **Advanced Analytics**: Learning progress tracking

### Planned Features
- **Multi-language Support**: Hindi, Tamil, Bengali, and other Indian languages
- **Visual Diagrams**: Auto-generate charts and diagrams for complex concepts
- **Progress Tracking**: Monitor learning progress and performance
- **Collaborative Learning**: Share documents and flashcards with classmates
- **Mobile App**: Native iOS and Android applications

## 🛡️ Security Features

- **Input Validation**: Comprehensive request validation
- **File Type Verification**: Only allow safe file uploads
- **CORS Configuration**: Secure cross-origin resource sharing
- **Error Handling**: Graceful error responses
- **UUID-based IDs**: Secure document identification

## 🏆 Key Achievements

✅ **Complete RAG Implementation**: Full pipeline from document upload to intelligent Q&A  
✅ **Multi-modal Input**: Support for both PDFs and YouTube videos  
✅ **Semantic Search**: Advanced AI-powered content retrieval  
✅ **Beautiful UI**: Modern, responsive, and intuitive interface  
✅ **Scalable Architecture**: Clean separation of concerns and modular design  
✅ **Production Ready**: Comprehensive error handling and testing  

## 📝 License

This project is designed for educational purposes and to support Indian students in their learning journey.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## 📞 Support

For questions, issues, or feature requests, please create an issue in the repository.

---

**Made with ❤️ for Indian Students** 🇮🇳

*Empowering every student with AI-powered personalized learning*
