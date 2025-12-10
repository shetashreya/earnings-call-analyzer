# Earnings Call Transcript Analyzer


AI-powered application that processes quarterly earnings call transcripts and generates concise, evidence-backed investment insights for each company. Users can upload multiple PDF transcripts, automatically extract and analyze key financial signals, and view:

- **3–4 line investability summary** for each company  
- **Reasons, sector tagging, and confidence scoring**  
- **Evidence excerpts** pulled directly from the transcript  
- **Side-by-side comparison** between companies  
- **Final investment recommendation** based on signals and retrieved context  


## Features

- **PDF Upload & Processing**: Upload quarterly earnings call transcripts (PDF)
- **Automatic Text Extraction**: Clean text extraction with chunking
- **Vector Embeddings**: Ollama mxbai-embed-large for semantic search
- **RAG Pipeline**: Context-aware analysis using Gemini API or Ollama
- **Investment Summaries**: 3-4 line summaries with investability assessment
- **Company Comparison**: Side-by-side analysis with recommendations
- **Simple UI**: Streamlit-based interface

## Tech Stack

- **Embeddings**: Ollama (mxbai-embed-large)
- **LLM**: Gemini API (primary) / Ollama llama3.2 (fallback)
- **Vector DB**: ChromaDB
- **PDF Processing**: pdfplumber, PyPDF2
- **UI**: Streamlit

## How to Use

### Upload & Analyze Companies

1. Navigate to **"Upload & Analyze"** page
2. Click **"Browse files"** and select PDF earnings call transcripts
3. Enter company names for each uploaded file
4. Click **"Process"** to extract and embed the content
5. Click **"Generate Analysis"** to get investment summary
6. View evidence excerpts supporting the analysis

### Compare Companies

1. Navigate to **"Compare Companies"** page
2. Select 2 or more companies from the dropdown
3. Click **"Compare Selected Companies"**
4. View side-by-side analyses and investment recommendation


<img width="1917" height="1033" alt="Screenshot 2025-12-06 231723" src="https://github.com/user-attachments/assets/e8e9529c-2e5a-4d6d-89f5-facb75add0d8" />
<br>
<img width="1471" height="1034" alt="Screenshot 2025-12-06 231906" src="https://github.com/user-attachments/assets/f74e1cb0-dd12-4a36-8c01-be23bcd86fcd" />


- LLM model
- Vector DB settings
