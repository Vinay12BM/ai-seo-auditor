// frontend/src/pages/Dashboard.jsx

import React, { useState } from 'react';
import InputForm from '../components/InputForm';
import ReportDisplay from '../components/ReportDisplay';

const API_BASE_URL = 'http://localhost:8000'; // Match your FastAPI server port

const Dashboard = () => {
  const [reportData, setReportData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // --- API Function: Analyze URL ---
  const handleAnalyze = async (url) => {
    setIsLoading(true);
    setReportData(null);
    setError(null);
    
    try {
      const response = await fetch(`${API_BASE_URL}/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      });

      const data = await response.json();

      if (!response.ok) {
        const errorMessage = await response.text();
        console.error('Backend Error:', errorMessage);
        throw new Error(errorMessage || 'Failed to get SEO analysis from backend.');
      }

      // Store the full report object from Gemini
      setReportData(data.seo_report);
      
    } catch (err) {
      console.error('Analysis Error:', err);
      setError(err.message || 'An unexpected error occurred during analysis.');
    } finally {
      setIsLoading(false);
    }
  };

  // --- API Function: Download PDF ---
  const handleDownload = async () => {
    if (!reportData) {
      setError('No report data available to download.');
      return;
    }
    setError(null);
    setIsLoading(true);
    
    try {
      const response = await fetch(`${API_BASE_URL}/download`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ seo_report: reportData }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(errorText || 'Failed to generate PDF.');
      }

      // Handle successful PDF blob response
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `SEO_Report_${new Date().toISOString().slice(0, 10)}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
      
    } catch (err) {
      console.error('Download Error:', err);
      setError(err.message || 'An error occurred during PDF download.');
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto">
        <header className="text-center mb-10">
          <h1 className="text-4xl font-extrabold text-gray-900">
            <span className="text-indigo-600">AI</span>-Powered SEO Auditor
          </h1>
          <p className="mt-2 text-lg text-gray-600">
            Autonomous crawling, Gemini analysis, and professional PDF reporting.
          </p>
        </header>

        {/* Error Display */}
        {error && (
          <div className="max-w-xl mx-auto p-4 mb-6 text-sm text-red-700 bg-red-100 rounded-lg shadow-md">
            <strong>Error:</strong> {error}
          </div>
        )}

        {/* Conditional Rendering */}
        {!reportData ? (
          // 1. Show Input Form
          <InputForm onAnalyze={handleAnalyze} isLoading={isLoading} />
        ) : (
          // 2. Show Report Display
          <ReportDisplay 
            report={reportData}
            isLoading={isLoading}
            onDownload={handleDownload}
          />
        )}

        {/* Option to start a new analysis */}
        {reportData && (
            <div className="text-center mt-8">
                <button
                    onClick={() => setReportData(null)}
                    className="text-indigo-600 hover:text-indigo-800 font-medium text-sm"
                >
                    Start New Analysis
                </button>
            </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;