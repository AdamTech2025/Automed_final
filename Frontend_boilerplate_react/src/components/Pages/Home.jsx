import { FaTooth, FaCogs, FaCheck, FaTimes, FaPaperPlane, FaRobot, FaCopy } from 'react-icons/fa';
import { analyzeDentalScenario, submitSelectedCodes, addCustomCode } from '../../interceptors/services.js';
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
  const [expandedTopics, setExpandedTopics] = useState({});
  const [newCode, setNewCode] = useState('');

  // Check if there are questions in the result
  useEffect(() => {
    if (result && (result.data.cdt_questions?.length > 0 || result.data.icd_questions?.length > 0)) {
      setShowQuestioner(true);
    } else {
      setShowQuestioner(false);
    }
  }, [result]);

  // At the beginning of the component, add a debug effect
  useEffect(() => {
    if (result?.data?.subtopics_data) {
      console.log("Subtopics data received:", result.data.subtopics_data);
      // Initialize expanded topics state
      const initialExpandedState = {};
      Object.keys(result.data.subtopics_data).forEach(topic => {
        initialExpandedState[topic] = false;
      });
      setExpandedTopics(initialExpandedState);
    }
  }, [result?.data?.subtopics_data]);

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

  const toggleTopic = (topic) => {
    console.log(`Toggling topic: ${topic}, current state:`, expandedTopics[topic]);
    setExpandedTopics(prev => {
      const newState = { ...prev };
      newState[topic] = !prev[topic];
      console.log(`New expanded state for ${topic}:`, newState[topic]);
      return newState;
    });
  };

  const handleCopyCodes = () => {
    const acceptedCodes = result.data.inspector_results.codes.join(', ');
    
    let textToCopy = `Accepted: ${acceptedCodes}`;
    
    navigator.clipboard.writeText(textToCopy).then(() => {
      alert('Codes copied to clipboard!');
    }).catch(err => {
      console.error('Failed to copy codes: ', err);
    });
  };

  const scrollToCode = (code) => {
    // Find the topic containing the code
    let foundTopic = null;
    let codeIndex = -1;
    
    // Search through all topics and their specific_codes to find the matching code
    Object.keys(result.data.subtopics_data).forEach(topic => {
      const topicData = result.data.subtopics_data[topic];
      if (topicData.specific_codes) {
        topicData.specific_codes.forEach((codeData, index) => {
          if (codeData && codeData.code === code) {
            foundTopic = topic;
            codeIndex = index;
          }
        });
      }
    });

    if (foundTopic) {
      console.log(`Found code ${code} in topic ${foundTopic} at index ${codeIndex}`);
      
      // Expand the topic if it's not already expanded
      if (!expandedTopics[foundTopic]) {
        setExpandedTopics(prev => ({
          ...prev,
          [foundTopic]: true
        }));
      }

      // Wait a short time for the expansion animation to complete before scrolling
      setTimeout(() => {
        // Scroll to the code
        const element = document.getElementById(`code-${code}`);
        if (element) {
          element.scrollIntoView({ behavior: 'smooth', block: 'center' });
          // Add a brief highlight effect
          element.classList.add('bg-yellow-100');
          setTimeout(() => {
            element.classList.remove('bg-yellow-100');
          }, 1500);
        } else {
          console.log(`Could not find element with ID code-${code}`);
        }
      }, 300);
    } else {
      console.log(`Could not find topic containing code ${code}`);
    }
  };

  const renderCodeSection = (topic) => {
    if (!result?.data?.subtopics_data?.[topic]) return null;
    
    const { topic_name, activated_subtopics, specific_codes } = result.data.subtopics_data[topic];
    const isExpanded = expandedTopics[topic];
    
    // Skip if no valid codes
    if (!specific_codes || specific_codes.length === 0) return null;
    
    // Skip if all codes are "none"
    const hasValidCodes = specific_codes.some(code => code && code.code && code.code !== 'none');
    if (!hasValidCodes) return null;
    
    return (
      <div className="mb-6">
        <div 
          className={`flex items-center justify-between p-4 ${topic === 'custom_codes' ? 'bg-blue-50' : 'bg-gray-50'} rounded-lg cursor-pointer hover:bg-gray-100 transition-colors`}
          onClick={() => toggleTopic(topic)}
        >
          <h3 className="text-lg font-semibold">{topic_name}</h3>
          <div className="transform transition-transform duration-300">
            {isExpanded ? '▼' : '▶'}
          </div>
        </div>
        
        <div className={`overflow-hidden transition-all duration-300 ease-in-out ${
          isExpanded ? 'max-h-[2000px] opacity-100' : 'max-h-0 opacity-0'
        }`}>
          {specific_codes.map((codeData, index) => {
            if (!codeData || !codeData.code || codeData.code === 'none') return null;

            const isAccepted = selectedCodes.accepted.includes(codeData.code);
            const isDenied = selectedCodes.denied.includes(codeData.code);
            
            // Determine which subtopic to use (if any)
            const subtopicText = activated_subtopics && activated_subtopics.length > index 
              ? activated_subtopics[index] 
              : codeData.code;

            return (
              <div 
                key={`topic-${index}-${topic}-${codeData.code}`}
                className={`mt-4 transition-all duration-300 ease-in-out ${
                  isAccepted ? 'bg-green-50 border-green-200' : 
                  isDenied ? 'bg-red-50 border-red-200' : 
                  'bg-white border-gray-200'
                }`}
              >
                <h4 className="font-medium text-gray-700 mb-2 p-4 flex justify-between items-center">
                  <span>{subtopicText}</span>
                  {topic === 'custom_codes' && 'isApplicable' in codeData && (
                    <span className={`text-sm px-2 py-1 rounded-full ${
                      codeData.isApplicable ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                    }`}>
                      {codeData.isApplicable ? 'Applicable' : 'Not Applicable'}
                    </span>
                  )}
                </h4>
                <div 
                  id={`code-${codeData.code}`} 
                  className={`p-4 rounded-lg shadow-sm border transition-colors duration-300 ${
                  isAccepted ? 'border-green-300' : 
                  isDenied ? 'border-red-300' : 
                  topic === 'custom_codes' && 'isApplicable' in codeData ? 
                    (codeData.isApplicable ? 'border-green-300' : 'border-red-300') :
                  'border-gray-200'
                }`}
                >
                  <div className="flex justify-between items-center mb-2">
                    <span className={`font-mono px-2 py-1 rounded ${
                      isAccepted ? 'bg-green-100 text-green-800' : 
                      isDenied ? 'bg-red-100 text-red-800' : 
                      topic === 'custom_codes' && 'isApplicable' in codeData ? 
                        (codeData.isApplicable ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800') :
                      'bg-gray-100 text-gray-800'
                    }`}>
                      {codeData.code}
                    </span>
                    <div className="flex space-x-2">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          handleCodeSelection(codeData.code, 'accept');
                        }}
                        className={`p-2 rounded-full transition-all duration-200 ${
                          isAccepted 
                            ? 'bg-green-500 text-white scale-110' 
                            : 'bg-gray-200 text-gray-600 hover:bg-green-500 hover:text-white hover:scale-110'
                        }`}
                      >
                        <FaCheck />
                      </button>
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          handleCodeSelection(codeData.code, 'deny');
                        }}
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
                    topic === 'custom_codes' && 'isApplicable' in codeData ? 
                      (codeData.isApplicable ? 'text-green-700' : 'text-red-700') :
                    'text-gray-600'
                  }`}>
                    <span className="font-medium">Explanation:</span> {codeData.explanation}
                  </p>
                  <p className={`text-sm ${
                    isAccepted ? 'text-green-700' : 
                    isDenied ? 'text-red-700' : 
                    topic === 'custom_codes' && 'isApplicable' in codeData ? 
                      (codeData.isApplicable ? 'text-green-700' : 'text-red-700') :
                    'text-gray-600'
                  }`}>
                    <span className="font-medium">Doubt:</span> {codeData.doubt}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    );
  };

  const renderInspectorResults = () => {
    if (!result?.data?.inspector_results) return null;

    const { codes, explanation } = result.data.inspector_results;

    return (
      <div className="mt-8 p-4 bg-blue-50 rounded-lg border border-blue-200 ai-final-analysis-content relative">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center">
            <FaRobot className="text-blue-500 mr-2" />
            <h3 className="text-lg font-semibold text-blue-700">AI Final Analysis</h3>
          </div>
          <button
            onClick={handleCopyCodes}
            className="text-blue-500 hover:text-blue-700 transition-colors"
          >
            <FaCopy className="inline mr-1" /> Copy Codes
          </button>
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
                  onClick={() => scrollToCode(code)}
                  className={`cursor-pointer px-3 py-1 rounded-full text-sm transition-all duration-200 ${
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
            // For custom codes, only count if applicable
            if (topic === 'custom_codes' && 'isApplicable' in codeData && !codeData.isApplicable) {
              return; // Skip this code
            }
            allCodes.push(codeData.code);
          }
        });
      }
    });
    
    // Check if all codes have been accepted
    return allCodes.length > 0 && allCodes.every(code => selectedCodes.accepted.includes(code));
  };

  // Add a function to get the count of remaining codes to select
  const getRemainingCodeCount = () => {
    if (!result?.data?.subtopics_data) return 0;
    
    // Count total valid codes
    let totalCodes = 0;
    let acceptedCount = 0;
    
    Object.keys(result.data.subtopics_data).forEach(topic => {
      const topicData = result.data.subtopics_data[topic];
      if (topicData.specific_codes) {
        topicData.specific_codes.forEach(codeData => {
          if (codeData && codeData.code && codeData.code !== 'none') {
            // For custom codes, only count if applicable
            if (topic === 'custom_codes' && 'isApplicable' in codeData && !codeData.isApplicable) {
              return; // Skip this code
            }
            totalCodes++;
            if (selectedCodes.accepted.includes(codeData.code)) {
              acceptedCount++;
            }
          }
        });
      }
    });
    
    return totalCodes - acceptedCount;
  };

  // Add a function to render the selected codes section
  const renderSelectedCodes = () => {
    if (selectedCodes.accepted.length === 0) return null;
    
    const handleCopySelectedCodes = () => {
      const acceptedText = selectedCodes.accepted.length > 0 
        ? `Accepted: ${selectedCodes.accepted.join(', ')}` 
        : '';
      
      navigator.clipboard.writeText(acceptedText);
      alert('Selected codes copied to clipboard!');
    };
    
    return (
      <div className="mt-8 p-4 bg-gray-50 rounded-lg border border-gray-200">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold">Your Selections</h3>
          <button
            onClick={handleCopySelectedCodes}
            className="text-blue-500 hover:text-blue-700 transition-colors flex items-center"
          >
            <FaCopy className="mr-1" /> Copy All
          </button>
        </div>
        
        {selectedCodes.accepted.length > 0 && (
          <div>
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
      </div>
    );
  };

  const handleAddCode = async () => {
    if (!newCode.trim()) {
      setError("Please enter a valid code");
      return;
    }
    
    if (!result?.data?.record_id) {
      setError("No active analysis session. Please analyze a scenario first.");
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      const response = await addCustomCode(newCode, scenario, result.data.record_id);
      console.log('Custom code response:', response);
      
      // Update the result with the new code
      if (response.data && response.data.code_data) {
        // Create a copy of the current result
        const updatedResult = {...result};
        
        // Add the new code to the appropriate topic or create a new topic
        const codeData = response.data.code_data;
        
        if (!updatedResult.data.subtopics_data) {
          updatedResult.data.subtopics_data = {};
        }
        
        // Extract applicability status from the explanation
        const isApplicable = codeData.explanation && codeData.explanation.includes("**Applicable?** Yes");
        
        // Extract reason from the explanation
        let reason = "";
        if (codeData.explanation) {
          const reasonMatch = codeData.explanation.match(/\*\*Reason\*\*: (.*?)($|\n)/);
          reason = reasonMatch ? reasonMatch[1].trim() : "";
        }
        
        // Either add to "Custom Codes" topic or create it
        if (!updatedResult.data.subtopics_data.custom_codes) {
          updatedResult.data.subtopics_data.custom_codes = {
            topic_name: "Custom Added Codes",
            specific_codes: []
          };
        }
        
        // Add the new code data with parsed information
        updatedResult.data.subtopics_data.custom_codes.specific_codes.push({
          code: codeData.code,
          explanation: reason || codeData.explanation,
          doubt: codeData.doubt || "None",
          isApplicable: isApplicable
        });
        
        // If there are inspector results, add the code there too if applicable
        if (updatedResult.data.inspector_results) {
          if (isApplicable) {
            // Add to accepted codes if applicable
            if (!updatedResult.data.inspector_results.codes.includes(codeData.code)) {
              updatedResult.data.inspector_results.codes.push(codeData.code);
            }
          }
        }
        
        // Update the result state
        setResult(updatedResult);
        
        // Expand the custom codes topic
        setExpandedTopics(prev => ({
          ...prev,
          custom_codes: true
        }));
        
        // Clear the input
        setNewCode('');
        
        // Auto-select only the applicable codes
        if (isApplicable) {
          handleCodeSelection(codeData.code, 'accept');
        }
      } else {
        setError("Received invalid response format from server");
      }
    } catch (err) {
      console.error('Error adding custom code:', err);
      setError(err.message || 'Failed to add custom code');
    } finally {
      setLoading(false);
    }
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
        <div className="w-full  p-4 md:p-6 bg-white rounded-lg shadow-lg">
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
                  className="bg-blue-600 text-white px-4 py-2 md:px-6 md:py-2 rounded-lg shadow-md hover:bg-blue-700 disabled:bg-gray-400 text-sm md:text-base transition-all duration-300"
                  disabled={loading}
                >
                  <FaCogs className="inline mr-2" />
                  {loading ? 'Analyzing...' : 'Analyze'}
                </button>
              </div>
            </form>

            {/* Inspector Results Section */}
            {renderInspectorResults()}
            
            {/* Selected Codes Section */}
            {renderSelectedCodes()}

            {/* Result */}
            {result && !showQuestioner && (
              <div className="mt-6">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-lg font-semibold">Analysis Results</h3>
                  <div className="text-sm text-gray-600">
                    Selected: {selectedCodes.accepted.length}
                  </div>
                </div>

                {/* Code Sections */}
                {result?.data?.subtopics_data && Object.keys(result.data.subtopics_data).length > 0 ? (
                  Object.keys(result.data.subtopics_data).map((topic, index) => (
                    <div key={`topic-container-${index}-${topic}`}>{renderCodeSection(topic)}</div>
                  ))
                ) : (
                  <div className="mt-4 p-4 bg-gray-50 rounded-lg">
                    <p className="text-gray-600">No code sections available for this analysis.</p>
                  </div>
                )}

                {/* Add Code Section */}
                <div className="mt-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
                  <h3 className="text-lg font-semibold mb-3">Add Custom Code</h3>
                  <div className="flex items-center mb-2">
                    <input
                      type="text"
                      placeholder="Enter CDT code (e.g., D1120)"
                      className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 text-sm md:text-base"
                      value={newCode}
                      onChange={(e) => setNewCode(e.target.value)}
                      disabled={loading}
                    />
                    <button
                      onClick={handleAddCode}
                      className="ml-2 px-4 py-2 bg-blue-600 text-white rounded-lg shadow-md hover:bg-blue-700 transition-all duration-300 disabled:bg-gray-400 flex items-center"
                      disabled={loading || !newCode.trim() || !result?.data?.record_id}
                    >
                      {loading ? 'Analyzing...' : 'Analyze Code'}
                    </button>
                  </div>
                  <p className="text-xs text-gray-500 mt-1">
                    Add a custom CDT code to check if it&apos;s applicable to this scenario.
                    The AI will analyze and provide a recommendation.
                  </p>
                </div>

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
                        ? 'Submit Accepted Codes' 
                        : `Accept All Codes (${getRemainingCodeCount()} remaining)`
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