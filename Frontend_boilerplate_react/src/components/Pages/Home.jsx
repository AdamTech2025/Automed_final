import { FaTooth, FaCogs, FaCheck, FaTimes, FaPaperPlane, FaRobot } from 'react-icons/fa';
import { analyzeDentalScenario, submitSelectedCodes } from '../../interceptors/services.js';
import { useState, useEffect } from 'react';
import Questioner from './Questioner.jsx';

const Home = () => {
  const [scenario, setScenario] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [selectedCodes, setSelectedCodes] = useState({ accepted: [], denied: [] });
  const [submitting, setSubmitting] = useState(false);
  const [showQuestioner, setShowQuestioner] = useState(false);

  // Check if there are questions in the result
  useEffect(() => {
    if (result && (result.data.cdt_questions?.length > 0 || result.data.icd_questions?.length > 0)) {
      setShowQuestioner(true);
    } else {
      setShowQuestioner(false);
    }
  }, [result]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);
    setSelectedCodes({ accepted: [], denied: [] });

    try {
      const response = await analyzeDentalScenario({ scenario });
      console.log('Analysis results received:', response);
      console.log('Record ID:', response?.data?.record_id);
      setResult(response);
    } catch (err) {
      console.error('Error analyzing scenario:', err);
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

  const handleQuestionerClose = () => {
    setShowQuestioner(false);
  };

  const handleQuestionerSuccess = (response) => {
    if (response && response.status === 'success') {
      // Only update result if we got a successful response
      setResult(response);
    } else if (response && response.status === 'error') {
      // Display the error message
      setError(response.message || 'Failed to process answers');
      // Don't hide the questioner modal on error
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
              key={`topic-${index}-${topic}`}
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
                  key={`code-${index}-${code}`}
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

  // Update the areAllCodesSelected function to count codes from subtopics_data instead
  const areAllCodesSelected = () => {
    if (!result?.data?.subtopics_data) return false;
    
    // Collect all valid codes from subtopics_data
    const allCodes = [];
    
    Object.keys(result.data.subtopics_data).forEach(topic => {
      const topicData = result.data.subtopics_data[topic];
      if (topicData.specific_codes) {
        topicData.specific_codes.forEach(codeData => {
          // Only count valid codes (not 'none')
          if (codeData && codeData.code && codeData.code !== 'none') {
            allCodes.push(codeData.code);
          }
        });
      }
    });
    
    const selectedCount = selectedCodes.accepted.length + selectedCodes.denied.length;
    
    // Check if every code has been either accepted or denied
    return allCodes.length > 0 && selectedCount === allCodes.length;
  };

  // Add a function to get the count of remaining codes to select
  const getRemainingCodeCount = () => {
    if (!result?.data?.subtopics_data) return 0;
    
    // Count total valid codes
    let totalCodes = 0;
    
    Object.keys(result.data.subtopics_data).forEach(topic => {
      const topicData = result.data.subtopics_data[topic];
      if (topicData.specific_codes) {
        topicData.specific_codes.forEach(codeData => {
          if (codeData && codeData.code && codeData.code !== 'none') {
            totalCodes++;
          }
        });
      }
    });
    
    const selectedCount = selectedCodes.accepted.length + selectedCodes.denied.length;
    return totalCodes - selectedCount;
  };

  // Add a function to render the selected codes section
  const renderSelectedCodes = () => {
    if (selectedCodes.accepted.length === 0 && selectedCodes.denied.length === 0) return null;
    
    return (
      <div className="mt-8 p-4 bg-gray-50 rounded-lg border border-gray-200">
        <h3 className="text-lg font-semibold mb-4">Your Selections</h3>
        
        {selectedCodes.accepted.length > 0 && (
          <div className="mb-4">
            <h4 className="font-medium text-green-700 mb-2">Accepted Codes:</h4>
            <div className="flex flex-wrap gap-2">
              {selectedCodes.accepted.map((code, index) => (
                <span 
                  key={`accepted-${index}-${code}`}
                  className="px-3 py-1 rounded-full text-sm bg-green-100 text-green-800 border border-green-300"
                >
                  {code}
                </span>
              ))}
            </div>
          </div>
        )}
        
        {selectedCodes.denied.length > 0 && (
          <div>
            <h4 className="font-medium text-red-700 mb-2">Denied Codes:</h4>
            <div className="flex flex-wrap gap-2">
              {selectedCodes.denied.map((code, index) => (
                <span 
                  key={`denied-${index}-${code}`}
                  className="px-3 py-1 rounded-full text-sm bg-red-100 text-red-800 border border-red-300"
                >
                  {code}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="flex flex-col bg-gray-100">
      {/* Questioner Modal */}
      {result && (
        <Questioner
          isVisible={showQuestioner}
          onClose={handleQuestionerClose}
          questions={{
            cdt_questions: result?.data?.cdt_questions || [],
            icd_questions: result?.data?.icd_questions || []
          }}
          recordId={result?.data?.record_id || ''}
          onSubmitSuccess={handleQuestionerSuccess}
        />
      )}

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
            {result && !showQuestioner && (
              <div className="mt-6">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-lg font-semibold">Analysis Results</h3>
                  <div className="text-sm text-gray-600">
                    Selected: {selectedCodes.accepted.length} | Denied: {selectedCodes.denied.length}
                  </div>
                </div>

                {/* Code Sections */}
                {Object.keys(result?.data?.subtopics_data || {}).map((topic, index) => (
                  <div key={`topic-${index}-${topic}`}>{renderCodeSection(topic)}</div>
                ))}

                {/* Inspector Results */}
                {renderInspectorResults()}

                {/* Selected Codes Section */}
                {renderSelectedCodes()}

                {/* Submit Button */}
                <div className="mt-6 flex justify-end">
                  <button
                    onClick={handleSubmitCodes}
                    disabled={submitting || !areAllCodesSelected()}
                    className={`px-4 py-2 rounded-lg shadow-md flex items-center transition-all duration-300 ${
                      areAllCodesSelected() 
                        ? 'bg-green-600 text-white hover:bg-green-700' 
                        : 'bg-gray-400 text-white cursor-not-allowed'
                    }`}
                  >
                    <FaPaperPlane className="mr-2" />
                    {submitting 
                      ? 'Submitting...' 
                      : areAllCodesSelected() 
                        ? 'Submit Selected Codes' 
                        : `Select All Codes (${getRemainingCodeCount()} remaining)`
                    }
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