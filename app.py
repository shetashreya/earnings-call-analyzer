import streamlit as st
import os
from pdf_processor import PDFProcessor
from vector_store import VectorStore
from analyzer import CompanyAnalyzer

st.set_page_config(page_title="Earnings Call Analyzer", layout="wide")

# Initialize components
@st.cache_resource
def get_components():
    return VectorStore(), CompanyAnalyzer()

vector_store, analyzer = get_components()

# Sidebar
st.sidebar.title("📊 Earnings Call Analyzer")
page = st.sidebar.radio("Navigation", ["Upload & Analyze", "Compare Companies"])

if page == "Upload & Analyze":
    st.title("Upload Earnings Call Transcripts")
    
    uploaded_files = st.file_uploader(
        "Upload PDF transcripts",
        type=['pdf'],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            company_name = st.text_input(
                f"Company name for {uploaded_file.name}",
                value=uploaded_file.name.replace('.pdf', ''),
                key=uploaded_file.name
            )
            
            if st.button(f"Process {uploaded_file.name}", key=f"btn_{uploaded_file.name}"):
                with st.spinner(f"Processing {company_name}..."):
                    # Save uploaded file temporarily
                    temp_path = f"temp_{uploaded_file.name}"
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Extract and process
                    text = PDFProcessor.extract_text(temp_path)
                    chunks = PDFProcessor.chunk_text(text)
                    
                    # Store in vector DB
                    vector_store.add_documents(company_name, chunks)
                    
                    # Clean up
                    os.remove(temp_path)
                    
                    st.success(f"✅ Processed {company_name} - {len(chunks)} chunks stored")
    
    st.divider()
    st.subheader("Company Summaries")
    
    companies = vector_store.get_companies()
    
    if companies:
        for company in companies:
            with st.expander(f"📈 {company}"):
                if st.button(f"Generate Analysis", key=f"analyze_{company}"):
                    with st.spinner("Analyzing..."):
                        try:
                            result = analyzer.analyze_company(company)
                            
                            st.markdown("### Analysis")
                            st.write(result['analysis'])
                            
                            st.markdown("### Evidence Excerpts")
                            for i, evidence in enumerate(result['evidence'], 1):
                                st.text_area(
                                    f"Excerpt {i}",
                                    evidence[:500] + "...",
                                    height=100,
                                    key=f"evidence_{company}_{i}"
                                )
                        except Exception as e:
                            st.error(f"Analysis failed: {str(e)}")
                            st.info("Make sure Ollama is running and your Gemini API key is set in .env file")
                
                if st.button(f"Delete {company}", key=f"delete_{company}"):
                    vector_store.delete_company(company)
                    st.rerun()
    else:
        st.info("No companies uploaded yet. Upload transcripts to get started.")

elif page == "Compare Companies":
    st.title("Compare Companies")
    
    companies = vector_store.get_companies()
    
    if len(companies) < 2:
        st.warning("Upload at least 2 companies to compare")
    else:
        selected = st.multiselect(
            "Select companies to compare",
            companies,
            default=companies[:min(3, len(companies))]
        )
        
        if len(selected) >= 2:
            if st.button("Compare Selected Companies"):
                with st.spinner("Comparing companies..."):
                    try:
                        comparison = analyzer.compare_companies(selected)
                        
                        st.markdown("## 🏆 Recommendation")
                        st.info(comparison['recommendation'])
                        
                        st.divider()
                        st.markdown("## Individual Analyses")
                        
                        cols = st.columns(len(selected))
                        for i, analysis in enumerate(comparison['analyses']):
                            with cols[i]:
                                st.markdown(f"### {analysis['company']}")
                                st.write(analysis['analysis'])
                                
                                with st.expander("View Evidence"):
                                    for j, evidence in enumerate(analysis['evidence'], 1):
                                        st.text_area(
                                            f"Excerpt {j}",
                                            evidence[:400] + "...",
                                            height=80,
                                            key=f"cmp_evidence_{i}_{j}"
                                        )
                    except Exception as e:
                        st.error(f"Comparison failed: {str(e)}")
                        st.info("Make sure Ollama is running and your Gemini API key is set in .env file")
        else:
            st.info("Select at least 2 companies to compare")
