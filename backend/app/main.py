# backend/app/main.py - CORRECTED VERSION

from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware # <<< MISSING IMPORT
from pydantic import BaseModel # <<< REQUIRED for /analyze POST body
from dotenv import load_dotenv

# Load environment variables (MUST BE NEAR THE TOP)
load_dotenv()

# Import services
from app.services.crawler import crawl_website_data        # <<< MISSING IMPORT
from app.services.gemini_analyzer import analyze_with_gemini # <<< MISSING IMPORT
from app.services.pdf_generator import generate_seo_pdf 

# --- FastAPI Initialization ---
app = FastAPI(title="AI SEO Auditor")

# --- CORS Configuration (Essential for connecting frontend on a different port) ---
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:5175"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Schema for Input ---
class AnalysisRequest(BaseModel):
    url: str

# --- Endpoints ---

@app.get("/")
def read_root():
    return {"status": "AI SEO Auditor Backend is running", "api_version": "1.0"}

# <<< CRITICAL MISSING ENDPOINT: /analyze >>>
@app.post("/analyze")
def analyze_url(request: AnalysisRequest):
    """Endpoint to trigger website crawl and Gemini SEO analysis."""
    url = request.url.strip()
    if not url.startswith(('http://', 'https://')):
        raise HTTPException(status_code=400, detail="URL must start with http:// or https://")
    
    crawled_data = crawl_website_data(url)
    if "error" in crawled_data:
        raise HTTPException(status_code=500, detail=crawled_data["error"])
    
    seo_report_data = analyze_with_gemini(crawled_data)
    
    if "error" in seo_report_data:
        raise HTTPException(status_code=500, detail=seo_report_data["error"])

    return {
        "crawled_data": crawled_data,
        "seo_report": seo_report_data
    }

# <<< EXISTING /download ENDPOINT (No changes needed) >>>
@app.post("/download")
def download_report(request: dict):
    # ... your existing PDF logic here ...
    report_data = request.get("seo_report")
    if not report_data:
         raise HTTPException(status_code=400, detail="Missing SEO report data.")
    
    try:
        pdf_bytes = generate_seo_pdf(report_data)

        return Response(
            content=pdf_bytes, 
            media_type="application/pdf", 
            headers={"Content-Disposition": "attachment; filename=AI_SEO_Audit_Report.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF Generation Failed: {e}")