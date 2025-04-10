import { FaTooth, FaCogs, FaCheck, FaTimes, FaPaperPlane, FaRobot } from 'react-icons/fa';
import { analyzeDentalScenario, submitSelectedCodes } from '../../interceptors/services.js';
import { useState } from 'react';

const Home = () => {
  const [scenario, setScenario] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [selectedCodes, setSelectedCodes] = useState({ accepted: [], denied: [] });
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);
    setSelectedCodes({ accepted: [], denied: [] });

    try {
      const response = await analyzeDentalScenario({ scenario });
      setResult(response);
    } catch (err) {
      setError(err.message || 'An error occurred while analyzing the scenario');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleCodeSelection = (code, action) => {
    setSelectedCodes(prev => {
      const newState = { ...prev };
      
      // Remove code from both lists if it exists
      newState.accepted = newState.accepted.filter(c => c !== code);
      newState.denied = newState.denied.filter(c => c !== code);
      
      // Add to appropriate list
      if (action === 'accept') {
        newState.accepted.push(code);
      } else if (action === 'deny') {
        newState.denied.push(code);
      }
      
      return newState;
    });
  };

  const handleSubmitCodes = async () => {
    setSubmitting(true);
    try {
      await submitSelectedCodes(selectedCodes, result.data.record_id);
      // Reset form after successful submission
      setScenario('');
      setResult(null);
      setSelectedCodes({ accepted: [], denied: [] });
    } catch (err) {
      setError(err.message || 'Failed to submit selected codes');
    } finally {
      setSubmitting(false);
    }
  };

  const renderCodeSection = (topic) => {
    if (!result?.data?.subtopics_data?.[topic]) return null;
    
    const { topic_name, activated_subtopics, specific_codes } = result.data.subtopics_data[topic];
    
    return (
      <div className="mb-6">
        <h3 className="text-lg font-semibold mb-2">{topic_name}</h3>
        {activated_subtopics.map((subtopic, index) => {
          const codeData = specific_codes[index];
          if (!codeData || codeData.code === 'none') return null;

          const isAccepted = selectedCodes.accepted.includes(codeData.code);
          const isDenied = selectedCodes.denied.includes(codeData.code);

          return (
            <div 
              key={index} 
              className={`mb-4 transition-all duration-300 ease-in-out ${
                isAccepted ? 'bg-green-50 border-green-200' : 
                isDenied ? 'bg-red-50 border-red-200' : 
                'bg-white border-gray-200'
              }`}
            >
              <h4 className="font-medium text-gray-700 mb-2 p-4">{subtopic}</h4>
              <div className={`p-4 rounded-lg shadow-sm border ${
                isAccepted ? 'border-green-300' : 
                isDenied ? 'border-red-300' : 
                'border-gray-200'
              }`}>
                <div className="flex justify-between items-center mb-2">
                  <span className={`font-mono px-2 py-1 rounded ${
                    isAccepted ? 'bg-green-100 text-green-800' : 
                    isDenied ? 'bg-red-100 text-red-800' : 
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {codeData.code}
                  </span>
                  <div className="flex space-x-2">
                    <button
                      onClick={() => handleCodeSelection(codeData.code, 'accept')}
                      className={`p-2 rounded-full transition-all duration-200 ${
                        isAccepted 
                          ? 'bg-green-500 text-white scale-110' 
                          : 'bg-gray-200 text-gray-600 hover:bg-green-500 hover:text-white hover:scale-110'
                      }`}
                    >
                      <FaCheck />
                    </button>
                    <button
                      onClick={() => handleCodeSelection(codeData.code, 'deny')}
                      className={`p-2 rounded-full transition-all duration-200 ${
                        isDenied 
                          ? 'bg-red-500 text-white scale-110' 
                          : 'bg-gray-200 text-gray-600 hover:bg-red-500 hover:text-white hover:scale-110'
                      }`}
                    >
                      <FaTimes />
                    </button>
                  </div>
                </div>
                <p className={`text-sm mb-1 ${
                  isAccepted ? 'text-green-700' : 
                  isDenied ? 'text-red-700' : 
                  'text-gray-600'
                }`}>
                  <span className="font-medium">Explanation:</span> {codeData.explanation}
                </p>
                <p className={`text-sm ${
                  isAccepted ? 'text-green-700' : 
                  isDenied ? 'text-red-700' : 
                  'text-gray-600'
                }`}>
                  <span className="font-medium">Doubt:</span> {codeData.doubt}
                </p>
              </div>
            </div>
          );
        })}
      </div>
    );
  };

  const renderInspectorResults = () => {
    if (!result?.data?.inspector_results) return null;

    const { codes, explanation } = result.data.inspector_results;

    return (
      <div className="mt-8 p-4 bg-blue-50 rounded-lg border border-blue-200">
        <div className="flex items-center mb-4">
          <FaRobot className="text-blue-500 mr-2" />
          <h3 className="text-lg font-semibold text-blue-700">AI Final Analysis</h3>
        </div>
        
        <div className="mb-4">
          <h4 className="font-medium text-gray-700 mb-2">Selected Codes:</h4>
          <div className="flex flex-wrap gap-2">
            {codes.map((code, index) => {
              const isAccepted = selectedCodes.accepted.includes(code);
              const isDenied = selectedCodes.denied.includes(code);
              
              return (
                <span 
                  key={index} 
                  className={`px-3 py-1 rounded-full text-sm transition-all duration-200 ${
                    isAccepted 
                      ? 'bg-green-100 text-green-800 border border-green-300' : 
                    isDenied 
                      ? 'bg-red-100 text-red-800 border border-red-300' : 
                      'bg-blue-100 text-blue-800'
                  }`}
                >
                  {code}
                </span>
              );
            })}
          </div>
        </div>

        <div>
          <h4 className="font-medium text-gray-700 mb-2">Explanation:</h4>
          <p className="text-sm text-gray-600">{explanation}</p>
        </div>
      </div>
    );
  };

  return (
    <div className="flex flex-col bg-gray-100">
      {/* Main content container */}
      <div className="flex-grow flex items-center justify-center p-4">
        <div className="w-full p-2 md:p-6 bg-white rounded-lg shadow-lg">
          {/* Header */}
          <div className="bg-blue-500 text-white p-4 rounded-lg mb-6">
            <h2 className="text-xl md:text-2xl font-semibold flex items-center">
              <FaTooth className="mr-2" /> Dental Scenario
            </h2>
          </div>

          {/* Form */}
          <div className="p-4">
            <form id="dental-form" className="space-y-4" onSubmit={handleSubmit}>
              <div>
                <label
                  htmlFor="scenario"
                  className="block text-gray-700 font-medium mb-2 text-sm md:text-base"
                >
                  Enter dental scenario to analyze:
                </label>
                <textarea
                  id="scenario"
                  name="scenario"
                  rows="6"
                  className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 text-sm md:text-base"
                  placeholder="Describe the dental procedure or diagnosis..."
                  value={scenario}
                  onChange={(e) => setScenario(e.target.value)}
                  onKeyDown={handleKeyDown}
                  required
                ></textarea>
              </div>
              <div className="flex justify-end">
                <button
                  type="submit"
                  className="bg-blue-600 text-white px-4 py-2 md:px-6 md:py-2 rounded-lg shadow-md hover:bg-blue-700 disabled:bg-gray-400 text-sm md:text-base"
                  disabled={loading}
                >
                  <FaCogs className="inline mr-2" />
                  {loading ? 'Analyzing...' : 'Analyze'}
                </button>
              </div>
            </form>

            {/* Result */}
            {result && (
              <div className="mt-6">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-lg font-semibold">Analysis Results</h3>
                  <div className="text-sm text-gray-600">
                    Selected: {selectedCodes.accepted.length} | Denied: {selectedCodes.denied.length}
                  </div>
                </div>

                {/* Code Sections */}
                {Object.keys(result.data.subtopics_data || {}).map(topic => renderCodeSection(topic))}

                {/* Inspector Results */}
                {renderInspectorResults()}

                {/* Submit Button */}
                <div className="mt-6 flex justify-end">
                  <button
                    onClick={handleSubmitCodes}
                    disabled={submitting || (selectedCodes.accepted.length === 0 && selectedCodes.denied.length === 0)}
                    className="bg-green-600 text-white px-4 py-2 rounded-lg shadow-md hover:bg-green-700 disabled:bg-gray-400 flex items-center"
                  >
                    <FaPaperPlane className="mr-2" />
                    {submitting ? 'Submitting...' : 'Submit Selected Codes'}
                  </button>
                </div>
              </div>
            )}

            {/* Error */}
            {error && (
              <div className="mt-4 p-4 bg-red-100 rounded-lg">
                <h3 className="font-semibold text-red-800 text-sm md:text-base">Error:</h3>
                <p className="text-xs md:text-sm">{error}</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;