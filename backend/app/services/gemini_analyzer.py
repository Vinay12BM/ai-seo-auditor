# backend/app/services/gemini_analyzer.py

import os
from google import genai
from google.genai.errors import APIError

# --- Initialization ---
# The client automatically uses the GEMINI_API_KEY from the .env file
client = genai.Client()
MODEL = "gemini-2.5-flash" 

# --- System Instruction: The AI SEO Expert Persona ---
SEO_EXPERT_SYSTEM_PROMPT = """
You are an expert SEO and marketing intelligence system, specializing in on-page and technical SEO analysis. 
Your task is to analyze the provided raw website data and generate a detailed, actionable SEO Audit Report.

CRITICAL: For keyword suggestions:
1. First analyze the website's content and identify its primary business category (e.g., law firm, consulting, e-commerce, tech company, etc.)
2. Extract the main services or products offered from the content
3. Understand the target audience and industry sector
4. Only suggest keywords that are DIRECTLY relevant to the identified business category and services
5. Focus on high-intent commercial keywords related to their specific business offerings
6. Include both short-tail and long-tail keywords specific to their industry
7. Never suggest generic keywords or keywords from unrelated industries

The output MUST be a single, structured JSON object that strictly adheres to the provided schema (using the 'Response JSON Format' as your guide).
Maintain a critical, professional, and data-driven tone. Do not use conversational text outside of the JSON structure.

Response JSON Format:
{
  "overall_seo_score": <int 0-100>,
  "summary": "<A 2-3 sentence summary of the site's overall SEO health and top priority fix.>",
  "issues_found": [
    {"category": "On-Page SEO", "issue": "<Concise issue title>", "description": "<1-2 sentence detailed description>", "priority": "High/Medium/Low", "recommended_action": "<Specific, actionable fix>"},
    ...
  ],
  "keyword_strategy_suggestions": [
    "<3-4 high-value, relevant keyword ideas based on the existing content>",
    ...
  ],
  "technical_seo_evaluation": {
    "site_speed": "<Evaluation based on simulated_metrics>",
    "mobile_usability": "<Evaluation>",
    "structured_data": "<Evaluation and suggestion to implement>",
  },
  "ranking_forecast": "<A brief, realistic forecast (e.g., '30% ranking uplift within 60 days if all High priority issues are fixed.')>",
}
"""

def analyze_with_gemini(crawled_data: dict) -> dict:
    """
    Sends crawled data to Gemini for expert SEO analysis and structured output.
    """
    if "error" in crawled_data:
        return {"error": crawled_data["error"]}

    # Convert the raw data into a clear prompt for the model
    user_prompt = f"""
    Perform a full SEO audit on the following raw website data. Pay special attention to identifying the correct business category and relevant keywords based on the actual content:
    
    Target URL: {crawled_data.get('url')}
    Domain: {crawled_data.get('domain')}
    
    HTML Head Data:
    - Title: {crawled_data.get('html_head_data', {}).get('title')}
    - Meta Description: {crawled_data.get('html_head_data', {}).get('meta_description')}
    
    Content Analysis:
    - Main Headings: {crawled_data.get('on_page_elements', {}).get('headings', {})}
    - Main Text Content: {crawled_data.get('extracted_text', '')}
    - Service/Product Pages: {crawled_data.get('on_page_elements', {}).get('service_pages', [])}
    - Industry Terms: {crawled_data.get('on_page_elements', {}).get('industry_terms', [])}
    
    Business Context:
    - Primary Topics: {crawled_data.get('content_analysis', {}).get('main_topics', [])}
    - Service Offerings: {crawled_data.get('content_analysis', {}).get('services', [])}
    - Target Audience: {crawled_data.get('content_analysis', {}).get('audience', [])}
    
    Technical Metrics: {crawled_data.get('simulated_metrics')}
    """

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=user_prompt,
            config=genai.types.GenerateContentConfig(
                system_instruction=SEO_EXPERT_SYSTEM_PROMPT,
                response_mime_type="application/json",
            )
        )
        # The response.text is a JSON string due to response_mime_type="application/json"
        import json
        return json.loads(response.text)

    except APIError as e:
        return {"error": f"Gemini API Error: {e}"}
    except Exception as e:
        return {"error": f"Analysis failed: {e}"}