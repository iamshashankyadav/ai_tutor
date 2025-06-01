
import requests
import os
import sys
import time
from pathlib import Path

class AITutorAPITester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.document_id = None
        
    def run_test(self, name, method, endpoint, expected_status, data=None, files=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {}
        
        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                if files:
                    response = requests.post(url, files=files)
                else:
                    response = requests.post(url, json=data, headers=headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    return success, response.json()
                except:
                    return success, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    print(f"Response: {response.text}")
                    return False, response.json()
                except:
                    return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}
    
    def test_root_endpoint(self):
        """Test the root API endpoint"""
        success, response = self.run_test(
            "Root API Endpoint",
            "GET",
            "api",
            200
        )
        return success
    
    def test_upload_pdf(self, pdf_path):
        """Test PDF upload functionality"""
        try:
            with open(pdf_path, 'rb') as pdf_file:
                files = {'file': (os.path.basename(pdf_path), pdf_file, 'application/pdf')}
                success, response = self.run_test(
                    "PDF Upload",
                    "POST",
                    "api/upload-pdf",
                    200,
                    files=files
                )
                if success and 'document_id' in response:
                    self.document_id = response['document_id']
                    print(f"Document ID: {self.document_id}")
                return success
        except Exception as e:
            print(f"❌ Failed to open PDF file: {str(e)}")
            return False
    
    def test_upload_youtube(self, youtube_url):
        """Test YouTube transcript processing"""
        success, response = self.run_test(
            "YouTube Upload",
            "POST",
            "api/upload-youtube",
            200,
            data={"youtube_url": youtube_url, "difficulty": "intermediate"}
        )
        if success and 'document_id' in response:
            self.document_id = response['document_id']
            print(f"Document ID: {self.document_id}")
        return success
    
    def test_ask_question(self, question, difficulty="intermediate"):
        """Test question answering"""
        success, response = self.run_test(
            "Ask Question",
            "POST",
            "api/ask-question",
            200,
            data={"question": question, "difficulty": difficulty}
        )
        if success:
            print(f"Answer: {response.get('answer', 'No answer provided')}")
        return success
    
    def test_get_documents(self):
        """Test document listing"""
        success, response = self.run_test(
            "Get Documents",
            "GET",
            "api/documents",
            200
        )
        if success and 'documents' in response:
            print(f"Found {len(response['documents'])} documents")
        return success
    
    def test_generate_flashcards(self):
        """Test flashcard generation"""
        if not self.document_id:
            print("❌ No document ID available for flashcard generation")
            return False
            
        success, response = self.run_test(
            "Generate Flashcards",
            "POST",
            f"api/generate-flashcards/{self.document_id}",
            200
        )
        if success and 'flashcards' in response:
            print(f"Generated {len(response['flashcards'])} flashcards")
        return success

def create_sample_pdf():
    """Create a sample PDF file for testing"""
    try:
        from reportlab.pdfgen import canvas
        
        pdf_path = "/tmp/sample.pdf"
        c = canvas.Canvas(pdf_path)
        c.drawString(100, 750, "Sample PDF for AI Tutor Testing")
        c.drawString(100, 700, "This is a test document with some educational content.")
        c.drawString(100, 650, "Machine learning is a subset of artificial intelligence.")
        c.drawString(100, 600, "Python is a popular programming language for data science.")
        c.save()
        
        print(f"✅ Created sample PDF at {pdf_path}")
        return pdf_path
    except Exception as e:
        print(f"❌ Failed to create sample PDF: {str(e)}")
        return None

def main():
    # Get backend URL from frontend .env
    env_path = Path("/app/frontend/.env")
    backend_url = None
    
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    backend_url = line.strip().split('=')[1].strip('"\'')
                    break
    
    if not backend_url:
        print("❌ Could not find REACT_APP_BACKEND_URL in frontend/.env")
        return 1
    
    print(f"🔗 Using backend URL: {backend_url}")
    
    # Setup
    tester = AITutorAPITester(backend_url)
    
    # Test root endpoint
    if not tester.test_root_endpoint():
        print("❌ Root API endpoint test failed, stopping tests")
        return 1
    
    # Create sample PDF and test upload
    pdf_path = create_sample_pdf()
    if pdf_path and not tester.test_upload_pdf(pdf_path):
        print("❌ PDF upload test failed")
    
    # Test YouTube upload
    if not tester.test_upload_youtube("https://www.youtube.com/watch?v=dQw4w9WgXcQ"):
        print("❌ YouTube upload test failed")
    
    # Test document listing
    if not tester.test_get_documents():
        print("❌ Document listing test failed")
    
    # Test question answering
    if not tester.test_ask_question("What is machine learning?"):
        print("❌ Question answering test failed")
    
    # Test flashcard generation
    if not tester.test_generate_flashcards():
        print("❌ Flashcard generation test failed")
    
    # Print results
    print(f"\n📊 Tests passed: {tester.tests_passed}/{tester.tests_run}")
    return 0 if tester.tests_passed == tester.tests_run else 1

if __name__ == "__main__":
    try:
        # Install reportlab if needed
        try:
            import reportlab
        except ImportError:
            print("Installing reportlab for PDF generation...")
            os.system("pip install reportlab")
        
        sys.exit(main())
    except Exception as e:
        print(f"❌ Unhandled exception: {str(e)}")
        sys.exit(1)
