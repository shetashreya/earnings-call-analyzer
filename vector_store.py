import chromadb
from chromadb.config import Settings
import requests
import json
from config import OLLAMA_BASE_URL, EMBEDDING_MODEL, CHROMA_PERSIST_DIR

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
        self.collection = self.client.get_or_create_collection(
            name="earnings_transcripts",
            metadata={"hnsw:space": "cosine"}
        )
    
    def get_embedding(self, text):
        """Get embeddings from Ollama"""
        try:
            response = requests.post(
                f"{OLLAMA_BASE_URL}/api/embeddings",
                json={"model": EMBEDDING_MODEL, "prompt": text},
                timeout=60
            )
            response.raise_for_status()
            result = response.json()
            if "embedding" in result:
                return result["embedding"]
            else:
                raise Exception(f"Unexpected embedding response: {result}")
        except Exception as e:
            raise Exception(f"Ollama embedding failed: {str(e)}. Make sure Ollama is running and model '{EMBEDDING_MODEL}' is available.")
    
    def add_documents(self, company_name, chunks):
        """Add document chunks to vector store"""
        for i, chunk in enumerate(chunks):
            embedding = self.get_embedding(chunk)
            self.collection.add(
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[{"company": company_name, "chunk_id": i}],
                ids=[f"{company_name}_{i}"]
            )
    
    def search(self, query, company_name=None, n_results=5):
        """Search for relevant chunks"""
        query_embedding = self.get_embedding(query)
        where_filter = {"company": company_name} if company_name else None
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where_filter
        )
        return results
    
    def get_companies(self):
        """Get list of all companies in the database"""
        all_data = self.collection.get()
        companies = set()
        if all_data and all_data['metadatas']:
            for metadata in all_data['metadatas']:
                companies.add(metadata['company'])
        return sorted(list(companies))
    
    def delete_company(self, company_name):
        """Delete all documents for a company"""
        results = self.collection.get(where={"company": company_name})
        if results['ids']:
            self.collection.delete(ids=results['ids'])
