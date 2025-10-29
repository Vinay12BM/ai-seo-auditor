// frontend/src/components/ReportDisplay.jsx

import React from 'react';

// Tailwind CSS utility function to determine color based on score/priority
const getScoreColor = (score) => {
  if (score >= 80) return 'bg-green-500';
  if (score >= 60) return 'bg-yellow-500';
  return 'bg-red-500';
};

const getPriorityColor = (priority) => {
  switch (priority) {
    case 'High':
      return 'bg-red-100 text-red-800';
    case 'Medium':
      return 'bg-yellow-100 text-yellow-800';
    case 'Low':
      return 'bg-green-100 text-green-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
};

const ReportDisplay = ({ report, onDownload, isLoading }) => {
  if (!report || !report.overall_seo_score) {
    return <div className="text-center text-gray-500">No SEO report data to display.</div>;
  }

  const {
    overall_seo_score,
    summary,
    issues_found,
    keyword_strategy_suggestions,
    technical_seo_evaluation,
    ranking_forecast,
  } = report;

  return (
    <div className="bg-white shadow-xl rounded-lg p-6 lg:p-10 mt-8 border border-gray-200">
      {/* Header and Score */}
      <div className="flex justify-between items-start border-b pb-4 mb-6">
        <div>
          <h1 className="text-3xl font-extrabold text-gray-900 flex items-center">
            <span className="mr-2">✨</span> AI SEO Audit Complete
          </h1>
          <p className="text-sm text-gray-500 mt-1">Autonomous analysis powered by Gemini.</p>
        </div>
        <div className={`p-4 rounded-full ${getScoreColor(overall_seo_score)} text-white font-bold text-4xl shadow-lg`}>
          {overall_seo_score}
          <span className="text-sm">/100</span>
        </div>
      </div>

      {/* Summary */}
      <div className="mb-8 p-4 bg-blue-50 border-l-4 border-blue-400 rounded-md">
        <h2 className="text-xl font-semibold text-blue-800 mb-2">Overall Summary</h2>
        <p className="text-gray-700">{summary}</p>
      </div>

      {/* Issues Table */}
      <h2 className="text-2xl font-bold text-gray-800 mb-4">🎯 Issues Found & Actions</h2>
      <div className="overflow-x-auto shadow-md rounded-lg mb-8">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Issue</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Priority</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Recommended Action</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {issues_found.map((issue, index) => (
              <tr key={index}>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm font-medium text-gray-900">{issue.issue}</div>
                  <div className="text-xs text-gray-500">{issue.description}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getPriorityColor(issue.priority)}`}>
                    {issue.priority}
                  </span>
                </td>
                <td className="px-6 py-4">
                  <p className="text-sm text-gray-600">{issue.recommended_action}</p>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Technical Evaluation & Forecast */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <div>
          <h2 className="text-2xl font-bold text-gray-800 mb-4">⚙️ Technical Evaluation</h2>
          {Object.entries(technical_seo_evaluation).map(([key, value]) => (
            <div key={key} className="flex justify-between py-2 border-b">
              <span className="font-semibold text-gray-700 capitalize">
                {key.replace(/_/g, ' ')}:
              </span>
              <span className="text-gray-600">{value}</span>
            </div>
          ))}
        </div>
        <div>
          <h2 className="text-2xl font-bold text-gray-800 mb-4">📈 Ranking Forecast & Keywords</h2>
          <div className="mb-4 p-3 bg-indigo-50 rounded-lg">
            <h3 className="font-semibold text-indigo-800">Forecast:</h3>
            <p className="text-sm text-gray-700">{ranking_forecast}</p>
          </div>
          <div className="p-3 bg-purple-50 rounded-lg">
            <h3 className="font-semibold text-purple-800 mb-2">Keyword Suggestions:</h3>
            <div className="flex flex-wrap gap-2">
              {keyword_strategy_suggestions.map((keyword, index) => (
                <span key={index} className="px-3 py-1 bg-purple-200 text-purple-800 text-xs font-medium rounded-full">
                  {keyword}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Download Button */}
      <button
        onClick={onDownload}
        disabled={isLoading}
        className={`w-full lg:w-auto mt-6 px-8 py-3 text-white font-semibold rounded-lg transition duration-150 shadow-md flex items-center justify-center ${
          isLoading ? 'bg-indigo-400 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-700'
        }`}
      >
        {isLoading ? (
          <>
            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Generating PDF...
          </>
        ) : (
          <>
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path>
            </svg>
            Download Professional SEO Report (PDF)
          </>
        )}
      </button>
    </div>
  );
};

export default ReportDisplay;