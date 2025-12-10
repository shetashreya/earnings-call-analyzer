import requests
import google.generativeai as genai
from config import OLLAMA_BASE_URL, LLM_MODEL, GEMINI_API_KEY
from vector_store import VectorStore

class RAGPipeline:
    def __init__(self, use_gemini=True):
        self.vector_store = VectorStore()
        self.use_gemini = use_gemini
        if use_gemini and GEMINI_API_KEY:
            genai.configure(api_key=GEMINI_API_KEY)
            self.gemini_model = genai.GenerativeModel('gemini-pro')
    
    def generate_with_ollama(self, prompt):
        """Generate response using Ollama"""
        try:
            response = requests.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={"model": LLM_MODEL, "prompt": prompt, "stream": False},
                timeout=120
            )
            response.raise_for_status()
            result = response.json()
            if "response" in result:
                return result["response"]
            else:
                raise Exception(f"Unexpected Ollama response format: {result}")
        except Exception as e:
            raise Exception(f"Ollama generation failed: {str(e)}")
    
    def generate_with_gemini(self, prompt):
        """Generate response using Gemini"""
        try:
            response = self.gemini_model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Gemini generation failed: {str(e)}")
    
    def generate(self, prompt):
        """Generate response using configured LLM"""
        if self.use_gemini and GEMINI_API_KEY:
            try:
                return self.generate_with_gemini(prompt)
            except Exception as e:
                print(f"Gemini failed, falling back to Ollama: {e}")
                return self.generate_with_ollama(prompt)
        return self.generate_with_ollama(prompt)
