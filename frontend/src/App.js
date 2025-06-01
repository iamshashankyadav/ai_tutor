import React, { useState, useEffect } from "react";
import "./App.css";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function App() {
  const [activeTab, setActiveTab] = useState("pdf");
  const [question, setQuestion] = useState("");
  const [difficulty, setDifficulty] = useState("intermediate");
  const [answer, setAnswer] = useState(null);
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [youtubeUrl, setYoutubeUrl] = useState("");
  const [flashcards, setFlashcards] = useState([]);
  const [currentFlashcard, setCurrentFlashcard] = useState(0);

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    try {
      const response = await axios.get(`${API}/documents`);
      setDocuments(response.data.documents);
    } catch (error) {
      console.error("Error fetching documents:", error);
    }
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(`${API}/upload-pdf`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      
      alert(`✅ ${response.data.message}\n📄 Processed ${response.data.chunks_processed} chunks`);
      fetchDocuments();
    } catch (error) {
      alert(`❌ Error: ${error.response?.data?.detail || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleYoutubeUpload = async () => {
    if (!youtubeUrl.trim()) {
      alert("Please enter a YouTube URL");
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(`${API}/upload-youtube`, {
        youtube_url: youtubeUrl,
        difficulty: difficulty
      });
      
      alert(`✅ ${response.data.message}\n📺 Processed ${response.data.chunks_processed} chunks`);
      setYoutubeUrl("");
      fetchDocuments();
    } catch (error) {
      alert(`❌ Error: ${error.response?.data?.detail || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleAskQuestion = async () => {
    if (!question.trim()) {
      alert("Please enter a question");
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(`${API}/ask-question`, {
        question: question,
        difficulty: difficulty
      });
      
      setAnswer(response.data);
    } catch (error) {
      alert(`❌ Error: ${error.response?.data?.detail || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const generateFlashcards = async (documentId) => {
    setLoading(true);
    try {
      const response = await axios.post(`${API}/generate-flashcards/${documentId}`);
      setFlashcards(response.data.flashcards);
      setCurrentFlashcard(0);
      setActiveTab("flashcards");
    } catch (error) {
      alert(`❌ Error: ${error.response?.data?.detail || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const nextFlashcard = () => {
    setCurrentFlashcard((prev) => (prev + 1) % flashcards.length);
  };

  const prevFlashcard = () => {
    setCurrentFlashcard((prev) => (prev - 1 + flashcards.length) % flashcards.length);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Header */}
      <header className="bg-white shadow-lg border-b-4 border-indigo-500">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center">
                <span className="text-white text-2xl font-bold">🧠</span>
              </div>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">AI Tutor</h1>
                <p className="text-gray-600">For Every Indian Student</p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">
                🇮🇳 Made for India
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Navigation Tabs */}
        <div className="mb-8">
          <nav className="flex space-x-1 bg-white rounded-xl p-1 shadow-lg">
            {[
              { id: "pdf", label: "📄 PDF Upload", icon: "📄" },
              { id: "youtube", label: "📺 YouTube", icon: "📺" },
              { id: "question", label: "❓ Ask Question", icon: "❓" },
              { id: "documents", label: "📚 Documents", icon: "📚" },
              { id: "flashcards", label: "🃏 Flashcards", icon: "🃏" }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex-1 py-3 px-4 rounded-lg font-medium transition-all duration-200 ${
                  activeTab === tab.id
                    ? "bg-indigo-500 text-white shadow-md"
                    : "text-gray-600 hover:text-indigo-600 hover:bg-indigo-50"
                }`}
              >
                {tab.label}
              </button>
            ))}
          </nav>
        </div>

        {/* Difficulty Selector */}
        <div className="mb-6 bg-white rounded-xl p-4 shadow-lg">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Difficulty Level:
          </label>
          <div className="flex space-x-4">
            {["beginner", "intermediate", "advanced"].map((level) => (
              <button
                key={level}
                onClick={() => setDifficulty(level)}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  difficulty === level
                    ? "bg-indigo-500 text-white"
                    : "bg-gray-100 text-gray-700 hover:bg-indigo-100"
                }`}
              >
                {level.charAt(0).toUpperCase() + level.slice(1)}
              </button>
            ))}
          </div>
        </div>

        {/* Content Areas */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          {/* PDF Upload Tab */}
          {activeTab === "pdf" && (
            <div className="space-y-6">
              <div className="text-center">
                <h2 className="text-2xl font-bold text-gray-900 mb-4">
                  📄 Upload PDF Document
                </h2>
                <p className="text-gray-600 mb-6">
                  Upload your textbooks, notes, or any PDF to get personalized learning assistance
                </p>
              </div>
              
              <div className="border-2 border-dashed border-indigo-300 rounded-xl p-8 text-center hover:border-indigo-400 transition-colors">
                <input
                  type="file"
                  accept=".pdf"
                  onChange={handleFileUpload}
                  className="hidden"
                  id="pdf-upload"
                  disabled={loading}
                />
                <label
                  htmlFor="pdf-upload"
                  className="cursor-pointer block"
                >
                  <div className="text-indigo-500 text-4xl mb-4">📄</div>
                  <p className="text-lg font-medium text-gray-700">
                    Click to upload PDF
                  </p>
                  <p className="text-gray-500 mt-2">
                    Supports PDF files up to 10MB
                  </p>
                </label>
              </div>
              
              {loading && (
                <div className="text-center py-4">
                  <div className="inline-flex items-center space-x-2">
                    <div className="animate-spin w-5 h-5 border-2 border-indigo-500 border-t-transparent rounded-full"></div>
                    <span>Processing PDF...</span>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* YouTube Tab */}
          {activeTab === "youtube" && (
            <div className="space-y-6">
              <div className="text-center">
                <h2 className="text-2xl font-bold text-gray-900 mb-4">
                  📺 YouTube Video Processing
                </h2>
                <p className="text-gray-600 mb-6">
                  Extract learning content from educational YouTube videos
                </p>
              </div>
              
              <div className="space-y-4">
                <input
                  type="url"
                  placeholder="Enter YouTube URL (e.g., https://youtube.com/watch?v=...)"
                  value={youtubeUrl}
                  onChange={(e) => setYoutubeUrl(e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  disabled={loading}
                />
                
                <button
                  onClick={handleYoutubeUpload}
                  disabled={loading || !youtubeUrl.trim()}
                  className="w-full bg-red-500 text-white py-3 px-6 rounded-lg font-medium hover:bg-red-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {loading ? "Processing..." : "📺 Process YouTube Video"}
                </button>
              </div>
            </div>
          )}

          {/* Question Tab */}
          {activeTab === "question" && (
            <div className="space-y-6">
              <div className="text-center">
                <h2 className="text-2xl font-bold text-gray-900 mb-4">
                  ❓ Ask Your Question
                </h2>
                <p className="text-gray-600 mb-6">
                  Get detailed explanations based on your uploaded content
                </p>
              </div>
              
              <div className="space-y-4">
                <textarea
                  placeholder="Ask any question about your uploaded documents..."
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  rows={4}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 resize-none"
                  disabled={loading}
                />
                
                <button
                  onClick={handleAskQuestion}
                  disabled={loading || !question.trim()}
                  className="w-full bg-indigo-500 text-white py-3 px-6 rounded-lg font-medium hover:bg-indigo-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {loading ? "Thinking..." : "🤔 Get Answer"}
                </button>
              </div>

              {/* Answer Display */}
              {answer && (
                <div className="bg-green-50 border border-green-200 rounded-xl p-6 space-y-4">
                  <div className="flex items-center justify-between">
                    <h3 className="text-lg font-semibold text-green-900">
                      ✅ Answer
                    </h3>
                    <span className="px-3 py-1 bg-green-200 text-green-800 rounded-full text-sm">
                      Confidence: {Math.round(answer.confidence * 100)}%
                    </span>
                  </div>
                  
                  <div className="space-y-3">
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">Answer:</h4>
                      <p className="text-gray-700">{answer.answer}</p>
                    </div>
                    
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">Explanation:</h4>
                      <p className="text-gray-700">{answer.explanation}</p>
                    </div>
                    
                    {answer.sources && answer.sources.length > 0 && (
                      <div>
                        <h4 className="font-medium text-gray-900 mb-2">Sources:</h4>
                        <ul className="list-disc list-inside text-gray-700 space-y-1">
                          {answer.sources.map((source, index) => (
                            <li key={index}>{source}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Documents Tab */}
          {activeTab === "documents" && (
            <div className="space-y-6">
              <div className="text-center">
                <h2 className="text-2xl font-bold text-gray-900 mb-4">
                  📚 Your Documents
                </h2>
                <p className="text-gray-600 mb-6">
                  Manage your uploaded PDFs and YouTube videos
                </p>
              </div>
              
              {documents.length === 0 ? (
                <div className="text-center py-12">
                  <div className="text-gray-400 text-6xl mb-4">📚</div>
                  <p className="text-gray-500">No documents uploaded yet</p>
                  <p className="text-gray-400 text-sm mt-2">Upload a PDF or process a YouTube video to get started</p>
                </div>
              ) : (
                <div className="grid gap-4">
                  {documents.map((doc) => (
                    <div key={doc.id} className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                          <span className="text-2xl">
                            {doc.content_type === "pdf" ? "📄" : "📺"}
                          </span>
                          <div>
                            <h3 className="font-medium text-gray-900">{doc.title}</h3>
                            <p className="text-sm text-gray-500">
                              {doc.chunks_count} chunks • {new Date(doc.upload_time).toLocaleDateString()}
                            </p>
                          </div>
                        </div>
                        <button
                          onClick={() => generateFlashcards(doc.id)}
                          disabled={loading}
                          className="px-4 py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600 disabled:opacity-50 text-sm"
                        >
                          🃏 Generate Flashcards
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Flashcards Tab */}
          {activeTab === "flashcards" && (
            <div className="space-y-6">
              <div className="text-center">
                <h2 className="text-2xl font-bold text-gray-900 mb-4">
                  🃏 Study Flashcards
                </h2>
                <p className="text-gray-600 mb-6">
                  Review key concepts with interactive flashcards
                </p>
              </div>
              
              {flashcards.length === 0 ? (
                <div className="text-center py-12">
                  <div className="text-gray-400 text-6xl mb-4">🃏</div>
                  <p className="text-gray-500">No flashcards generated yet</p>
                  <p className="text-gray-400 text-sm mt-2">Generate flashcards from your documents</p>
                </div>
              ) : (
                <div className="max-w-2xl mx-auto">
                  <div className="bg-gradient-to-r from-purple-500 to-indigo-600 rounded-xl p-8 text-white shadow-lg">
                    <div className="text-center mb-6">
                      <span className="text-purple-200 text-sm">
                        Card {currentFlashcard + 1} of {flashcards.length}
                      </span>
                    </div>
                    
                    <div className="space-y-6">
                      <div>
                        <h3 className="text-lg font-semibold mb-3">Question:</h3>
                        <p className="text-purple-100">{flashcards[currentFlashcard]?.question}</p>
                      </div>
                      
                      <div>
                        <h3 className="text-lg font-semibold mb-3">Answer:</h3>
                        <p className="text-purple-100">{flashcards[currentFlashcard]?.answer}</p>
                      </div>
                    </div>
                    
                    <div className="flex justify-between mt-8">
                      <button
                        onClick={prevFlashcard}
                        disabled={flashcards.length <= 1}
                        className="px-6 py-2 bg-white bg-opacity-20 text-white rounded-lg hover:bg-opacity-30 disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        ← Previous
                      </button>
                      <button
                        onClick={nextFlashcard}
                        disabled={flashcards.length <= 1}
                        className="px-6 py-2 bg-white bg-opacity-20 text-white rounded-lg hover:bg-opacity-30 disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        Next →
                      </button>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-50 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center">
            <p className="text-gray-600">
              🧠 AI Tutor - Empowering Indian students with personalized learning
            </p>
            <p className="text-gray-500 text-sm mt-2">
              Upload documents, ask questions, and learn with AI assistance
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
