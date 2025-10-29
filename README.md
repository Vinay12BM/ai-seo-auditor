# AI SEO Auditor

An AI-powered SEO analysis tool that provides comprehensive website audits using Google's Gemini API. The tool crawls websites, analyzes SEO factors, and generates professional PDF reports.

## Features

- 🔍 Autonomous website crawling
- 🤖 AI-powered SEO analysis using Google Gemini
- 📊 Comprehensive SEO scoring
- 📝 Professional PDF report generation
- 🎯 Actionable recommendations
- 📱 Mobile-responsive interface

## Tech Stack

### Frontend
- React with Vite
- TailwindCSS for styling
- Modern ES6+ JavaScript

### Backend
- FastAPI (Python)
- Google Gemini API for AI analysis
- ReportLab for PDF generation
- BeautifulSoup4 for web scraping

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 14+
- Google Gemini API key

### Installation

1. Clone the repository:
\`\`\`bash
git clone https://github.com/Vinay12BM/ai-seo-auditor.git
cd ai-seo-auditor
\`\`\`

2. Set up the backend:
\`\`\`bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
\`\`\`

3. Configure environment variables:
Create a \`.env\` file in the backend directory with:
\`\`\`
GEMINI_API_KEY=your_api_key_here
\`\`\`

4. Set up the frontend:
\`\`\`bash
cd frontend
npm install
\`\`\`

### Running the Application

1. Start the backend server:
\`\`\`bash
cd backend
uvicorn app.main:app --reload
\`\`\`

2. Start the frontend development server:
\`\`\`bash
cd frontend
npm run dev
\`\`\`

The application will be available at http://localhost:5173

## Usage

1. Enter a website URL in the input field
2. Click "Analyze Website" to start the SEO audit
3. View the comprehensive analysis results
4. Download the professional PDF report

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Gemini API for AI capabilities
- FastAPI for the efficient backend
- React and Vite for the modern frontend
- TailwindCSS for the sleek UI