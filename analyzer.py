from rag_pipeline import RAGPipeline

class CompanyAnalyzer:
    def __init__(self):
        self.rag = RAGPipeline(use_gemini=True)
    
    def analyze_company(self, company_name):
        """Generate investment summary for a company"""
        search_results = self.rag.vector_store.search(
            query="financial performance revenue growth profitability outlook risks",
            company_name=company_name,
            n_results=10
        )
        
        context = "\n\n".join(search_results['documents'][0])
        
        prompt = f"""Based on the following earnings call transcript excerpts for {company_name}, provide:
1. A 3-4 line investment summary
2. Whether the company is investable (Yes/No/Maybe)
3. The primary sector/industry
4. Key reasons (2-3 bullet points)

Context:
{context[:4000]}

Format your response as:
INVESTABLE: [Yes/No/Maybe]
SECTOR: [sector name]
SUMMARY: [3-4 line summary]
REASONS:
- [reason 1]
- [reason 2]
- [reason 3]
"""
        
        response = self.rag.generate(prompt)
        evidence = search_results['documents'][0][:3]
        
        return {
            "company": company_name,
            "analysis": response,
            "evidence": evidence
        }
    
    def compare_companies(self, company_names):
        """Compare multiple companies and recommend best investment"""
        analyses = []
        for company in company_names:
            analysis = self.analyze_company(company)
            analyses.append(analysis)
        
        comparison_text = "\n\n".join([
            f"{a['company']}:\n{a['analysis']}" for a in analyses
        ])
        
        prompt = f"""Compare these companies and recommend which one to invest in:

{comparison_text}

Provide:
1. Side-by-side comparison of key metrics
2. Recommended company to invest in
3. Clear reasoning (3-4 lines)

Format:
RECOMMENDATION: [Company Name]
REASONING: [explanation]
COMPARISON:
[comparison details]
"""
        
        recommendation = self.rag.generate(prompt)
        
        return {
            "analyses": analyses,
            "recommendation": recommendation
        }
