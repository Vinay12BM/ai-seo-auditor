// frontend/src/components/InputForm.jsx

import React, { useState } from 'react';

const InputForm = ({ onAnalyze, isLoading }) => {
  const [url, setUrl] = useState('');
  const [error, setError] = useState(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    setError(null);

    if (!url.startsWith('http://') && !url.startsWith('https://')) {
      setError('Please enter a valid URL starting with http:// or https://');
      return;
    }

    onAnalyze(url);
  };

  return (
    <div className="max-w-xl mx-auto p-8 bg-white shadow-xl rounded-xl border border-gray-200">
      <h2 className="text-2xl font-bold text-gray-800 mb-2">Autonomous SEO Audit</h2>
      <p className="text-gray-500 mb-6">Enter a website URL to initiate the Gemini-powered analysis.</p>

      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="website-url" className="block text-sm font-medium text-gray-700">
            Website URL (e.g., https://example.com)
          </label>
          <input
            type="url"
            id="website-url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            required
            placeholder="https://yourwebsite.com"
            className="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-indigo-500 focus:border-indigo-500 text-gray-900"
          />
        </div>

        {error && (
          <div className="p-3 mb-4 text-sm text-red-700 bg-red-100 rounded-lg">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={isLoading}
          className={`w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white transition duration-150 ${
            isLoading 
              ? 'bg-indigo-400 cursor-not-allowed' 
              : 'bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500'
          }`}
        >
          {isLoading ? (
            <div className="flex items-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Analyzing SEO... (May take 10-20s)
            </div>
          ) : (
            'Analyze Website'
          )}
        </button>
      </form>
    </div>
  );
};

export default InputForm;