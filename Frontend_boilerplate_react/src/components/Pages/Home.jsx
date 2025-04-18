import { FaTooth, FaCogs, FaCheck, FaTimes, FaPaperPlane, FaRobot, FaCopy, FaSpinner } from 'react-icons/fa';
import { analyzeDentalScenario, submitSelectedCodes, addCustomCode } from '../../interceptors/services.js';
import { useState, useEffect, useMemo } from 'react';
import Questioner from './Questioner.jsx';
import { useTheme } from '../../context/ThemeContext';

const Home = () => {
  const { isDark } = useTheme();
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
    if (result && result.questioner_data && result.questioner_data.has_questions) {
      setShowQuestioner(true);
    } else {
      setShowQuestioner(false);
    }
  }, [result]);

  // Transform CDT_subtopic array into the object format needed by the component
  const formattedSubtopicData = useMemo(() => {
    if (!result?.CDT_subtopic) {
      return {};
    }
    const formatted = {};
    result.CDT_subtopic.forEach(topic => {
      // Use a combination of topic name and code range as the key if possible
      const key = `${topic.topic || 'Unknown'} (${topic.code_range || 'N/A'})`;
      // Ensure the codes array exists and has data
      if (Array.isArray(topic.codes) && topic.codes.length > 0) {
        formatted[key] = topic.codes;
      }
    });
    return formatted;
  }, [result?.CDT_subtopic]);

  // Initialize expanded topics state based on the formatted data
  useEffect(() => {
    if (formattedSubtopicData && Object.keys(formattedSubtopicData).length > 0) {
      console.log("Formatted Subtopics data:", formattedSubtopicData);
      // Initialize expanded topics state
      const initialExpandedState = {};
      Object.keys(formattedSubtopicData).forEach(topicKey => {
        initialExpandedState[topicKey] = false; // Use the generated key
      });
      setExpandedTopics(initialExpandedState);
    } else {
        setExpandedTopics({}); // Reset if no data
    }
  }, [formattedSubtopicData]); // Depend on the formatted data

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);
    setSelectedCodes({ accepted: [], denied: [] });

    try {
      const response = await analyzeDentalScenario({ scenario });
      console.log('Analysis results received:', response);
      console.log('Record ID:', response?.record_id);
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
      await submitSelectedCodes(selectedCodes, result.record_id);
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
    // If response is an array (batch), check if ALL were successful
    const allSuccess = Array.isArray(response)
      ? response.every(r => r.response && r.response.status === 'success')
      : response && response.status === 'success';

    if (allSuccess) {
       // For batch, we might need to update the result state based on multiple responses.
       // For now, let's assume a single response structure or handle the first successful one for simplicity.
      const mainResponse = Array.isArray(response) ? response.find(r => r.response && r.response.status === 'success')?.response : response;
      if (mainResponse) {
          setResult(mainResponse); // Update result with the data returned AFTER answering questions
      }
    } else {
      // Handle single or batch error
      const errorMsg = Array.isArray(response)
        ? response.find(r => r.response && r.response.status === 'error')?.response?.message || 'An error occurred in batch processing.'
        : response?.message || 'Failed to process answers';
      setError(errorMsg);
      // Don't hide the questioner modal on error
    }
  };

  const toggleTopic = (topicKey) => {
    console.log(`Toggling topic: ${topicKey}, current state:`, expandedTopics[topicKey]);
    setExpandedTopics(prev => {
      const newState = { ...prev };
      newState[topicKey] = !prev[topicKey];
      console.log(`New expanded state for ${topicKey}:`, newState[topicKey]);
      return newState;
    });
  };

  const handleCopyCodes = () => {
    if (!result?.inspector_results) return;
    
    // Get the actual inspector results object (already direct)
    const inspectorData = result.inspector_results;
    
    const cdtCodes = inspectorData.cdt?.codes || [];
    const icdCodes = inspectorData.icd?.codes || [];
    
    let textToCopy = `CDT Codes: ${cdtCodes.join(', ')}\nICD Codes: ${icdCodes.join(', ')}`;
    
    navigator.clipboard.writeText(textToCopy).then(() => {
      alert('Codes copied to clipboard!');
    }).catch(err => {
      console.error('Failed to copy codes: ', err);
    });
  };

  const scrollToCode = (code) => {
    // Find the topic containing the code using formattedSubtopicData
    let foundTopicKey = null;
    let codeIndex = -1;
    
    // Search through the formatted data
    if (formattedSubtopicData) {
      Object.keys(formattedSubtopicData).forEach(topicKey => {
        const topicCodes = formattedSubtopicData[topicKey];
        if (topicCodes) {
          topicCodes.forEach((codeData, index) => {
            if (codeData && codeData.code === code) {
              foundTopicKey = topicKey;
              codeIndex = index;
            }
          });
        }
      });
    }

    if (foundTopicKey) {
      console.log(`Found code ${code} in topic ${foundTopicKey} at index ${codeIndex}`);
      
      // Expand the topic if it's not already expanded
      if (!expandedTopics[foundTopicKey]) {
        setExpandedTopics(prev => ({
          ...prev,
          [foundTopicKey]: true
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

  const renderCodeSection = (topicKey) => {
    if (!formattedSubtopicData?.[topicKey]) return null;
    
    const topicData = formattedSubtopicData[topicKey];
    const isExpanded = expandedTopics[topicKey];
    
    // Extract name from the key (assuming format "Name (Range)")
    const topicName = topicKey.split('(')[0].trim();
    
    // Skip if no valid codes
    if (!topicData || topicData.length === 0) return null;
    
    // Skip if all codes are "none"
    const hasValidCodes = topicData.some(code => code && code.code && code.code !== 'none' && code.code.toLowerCase() !== 'none');
    if (!hasValidCodes) return null;
    
    return (
      <div className="mb-6">
        <div 
          className={`flex items-center justify-between p-4 ${topicKey.includes('custom_codes') ? 
            (isDark ? 'bg-blue-900/30' : 'bg-blue-50') : 
            (isDark ? 'bg-gray-800' : 'bg-gray-50')
          } rounded-lg cursor-pointer hover:${isDark ? 'bg-gray-700' : 'bg-gray-100'} transition-colors`}
          onClick={() => toggleTopic(topicKey)}
        >
          <h3 className="text-lg font-semibold">{topicName}</h3>
          <div className="transform transition-transform duration-300">
            {isExpanded ? '▼' : '▶'}
          </div>
        </div>
        
        <div className={`overflow-hidden transition-all duration-300 ease-in-out ${
          isExpanded ? 'max-h-[2000px] opacity-100' : 'max-h-0 opacity-0'
        }`}>
          {topicData.map((codeData, index) => {
            if (!codeData || !codeData.code || codeData.code === 'none' || codeData.code.toLowerCase() === 'none') return null;

            const isAccepted = selectedCodes.accepted.includes(codeData.code);
            const isDenied = selectedCodes.denied.includes(codeData.code);
            
            return (
              <div 
                key={`topic-${index}-${topicKey}-${codeData.code}`}
                className={`mt-4 transition-all duration-300 ease-in-out ${
                  isAccepted ? (isDark ? 'bg-green-900/30 border-green-700' : 'bg-green-50 border-green-200') : 
                  isDenied ? (isDark ? 'bg-red-900/30 border-red-700' : 'bg-red-50 border-red-200') : 
                  (isDark ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200')
                }`}
              >
                <div 
                  id={`code-${codeData.code}`} 
                  className={`p-4 rounded-lg shadow-sm border transition-colors duration-300 ${
                  isAccepted ? (isDark ? 'border-green-700' : 'border-green-300') : 
                  isDenied ? (isDark ? 'border-red-700' : 'border-red-300') : 
                  topicKey.includes('custom_codes') && 'isApplicable' in codeData ? 
                    (codeData.isApplicable ? 
                      (isDark ? 'border-green-700' : 'border-green-300') : 
                      (isDark ? 'border-red-700' : 'border-red-300')
                    ) :
                  (isDark ? 'border-gray-700' : 'border-gray-200')
                }`}
                >
                  <div className="flex justify-between items-center mb-2">
                    <span className={`font-mono px-2 py-1 rounded ${
                      isAccepted ? (isDark ? 'bg-green-900 text-green-200' : 'bg-green-100 text-green-800') : 
                      isDenied ? (isDark ? 'bg-red-900 text-red-200' : 'bg-red-100 text-red-800') : 
                      topicKey.includes('custom_codes') && 'isApplicable' in codeData ? 
                        (codeData.isApplicable ? 
                          (isDark ? 'bg-green-900 text-green-200' : 'bg-green-100 text-green-800') : 
                          (isDark ? 'bg-red-900 text-red-200' : 'bg-red-100 text-red-800')
                        ) :
                      (isDark ? 'bg-gray-700 text-gray-200' : 'bg-gray-100 text-gray-800')
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
                            : (isDark ? 'bg-gray-700 text-gray-300' : 'bg-gray-200 text-gray-600') + ' hover:bg-green-500 hover:text-white hover:scale-110'
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
                            : (isDark ? 'bg-gray-700 text-gray-300' : 'bg-gray-200 text-gray-600') + ' hover:bg-red-500 hover:text-white hover:scale-110'
                        }`}
                      >
                        <FaTimes />
                      </button>
                    </div>
                  </div>
                  <p className={`text-sm mb-1 ${
                    isAccepted ? (isDark ? 'text-green-300' : 'text-green-700') : 
                    isDenied ? (isDark ? 'text-red-300' : 'text-red-700') : 
                    topicKey.includes('custom_codes') && 'isApplicable' in codeData ? 
                      (codeData.isApplicable ? 
                        (isDark ? 'text-green-300' : 'text-green-700') : 
                        (isDark ? 'text-red-300' : 'text-red-700')
                      ) :
                    (isDark ? 'text-gray-300' : 'text-gray-600')
                  }`}>
                    <span className="font-medium">Explanation:</span> {codeData.explanation || 'N/A'}
                  </p>
                  <p className={`text-sm ${
                    isAccepted ? (isDark ? 'text-green-300' : 'text-green-700') : 
                    isDenied ? (isDark ? 'text-red-300' : 'text-red-700') : 
                    topicKey.includes('custom_codes') && 'isApplicable' in codeData ? 
                      (codeData.isApplicable ? 
                        (isDark ? 'text-green-300' : 'text-green-700') : 
                        (isDark ? 'text-red-300' : 'text-red-700')
                      ) :
                    (isDark ? 'text-gray-300' : 'text-gray-600')
                  }`}>
                    <span className="font-medium">Doubt:</span> {codeData.doubt || 'N/A'}
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
    if (!result?.inspector_results) return null;

    // Get the actual inspector results object (already direct)
    const inspectorData = result.inspector_results;

    const cdtCodes = inspectorData.cdt?.codes || [];
    const icdCodes = inspectorData.icd?.codes || [];
    const cdtExplanation = inspectorData.cdt?.explanation || '';
    const icdExplanation = inspectorData.icd?.explanation || '';

    // Count CDT code occurrences
    const cdtCodeCounts = cdtCodes.reduce((acc, code) => {
      acc[code] = (acc[code] || 0) + 1;
      return acc;
    }, {});

    return (
      <div className={`mt-8 p-4 ${isDark ? 'bg-blue-900/30 border-blue-700' : 'bg-blue-50 border-blue-200'} rounded-lg border ai-final-analysis-content relative`}>
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center">
            <FaRobot className={`${isDark ? 'text-blue-400' : 'text-blue-500'} mr-2`} />
            <h3 className={`text-lg font-semibold ${isDark ? 'text-blue-400' : 'text-blue-700'}`}>AI Final Analysis</h3>
          </div>
          <button
            onClick={handleCopyCodes}
            className={`${isDark ? 'text-blue-400 hover:text-blue-300' : 'text-blue-500 hover:text-blue-700'} transition-colors`}
          >
            <FaCopy className="inline mr-1" /> Copy Codes
          </button>
        </div>
        
        <div className="mb-4">
          <h4 className={`font-medium ${isDark ? 'text-gray-200' : 'text-gray-700'} mb-2`}>CDT Codes:</h4>
          <div className="flex flex-wrap gap-2">
            {Object.entries(cdtCodeCounts).map(([code, count]) => {
              const isAccepted = selectedCodes.accepted.includes(code);
              const isDenied = selectedCodes.denied.includes(code);
              
              return (
                <span 
                  key={`cdt-code-${code}`}
                  onClick={() => scrollToCode(code)}
                  className={`cursor-pointer px-3 py-1 rounded-full text-sm transition-all duration-200 ${
                    isAccepted 
                      ? (isDark ? 'bg-green-900/60 text-green-200 border-green-700' : 'bg-green-100 text-green-800 border border-green-300') 
                      : isDenied 
                        ? (isDark ? 'bg-red-900/60 text-red-200 border-red-700' : 'bg-red-100 text-red-800 border border-red-300')
                        : (isDark ? 'bg-blue-800/60 text-blue-200' : 'bg-blue-100 text-blue-800')
                  }`}
                >
                  {code}{count > 1 ? ` (${count} Times)` : ''}
                </span>
              );
            })}
          </div>
          <p className={`text-sm ${isDark ? 'text-gray-300' : 'text-gray-600'} mt-2`}>{cdtExplanation}</p>
        </div>

        <div className="mb-4">
          <h4 className={`font-medium ${isDark ? 'text-gray-200' : 'text-gray-700'} mb-2`}>ICD Codes:</h4>
          <div className="flex flex-wrap gap-2">
            {icdCodes.map((code, index) => (
              <span 
                key={`icd-code-${index}-${code}`}
                className={`px-3 py-1 rounded-full text-sm ${
                  isDark ? 'bg-purple-900/60 text-purple-200' : 'bg-purple-100 text-purple-800'
                }`}
              >
                {code}
              </span>
            ))}
          </div>
          <p className={`text-sm ${isDark ? 'text-gray-300' : 'text-gray-600'} mt-2`}>{icdExplanation}</p>
        </div>
      </div>
    );
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
      <div className={`mt-8 p-4 ${isDark ? 'bg-gray-800 border-gray-700' : 'bg-gray-50 border-gray-200'} rounded-lg border`}>
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold">Your Selections</h3>
          <button
            onClick={handleCopySelectedCodes}
            className={`${isDark ? 'text-blue-400 hover:text-blue-300' : 'text-blue-500 hover:text-blue-700'} transition-colors flex items-center`}
          >
            <FaCopy className="mr-1" /> Copy All
          </button>
        </div>
        
        {selectedCodes.accepted.length > 0 && (
          <div>
            <h4 className={`font-medium ${isDark ? 'text-green-400' : 'text-green-700'} mb-2`}>Accepted Codes:</h4>
            <div className="flex flex-wrap gap-2">
              {selectedCodes.accepted.map((code, index) => (
                <span 
                  key={`accepted-${index}-${code}`}
                  className={`px-3 py-1 rounded-full text-sm ${
                    isDark ? 'bg-green-900/60 text-green-200 border border-green-700' : 'bg-green-100 text-green-800 border border-green-300'
                  }`}
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
    
    if (!result?.record_id) {
      setError("No active analysis session. Please analyze a scenario first.");
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      const response = await addCustomCode(newCode, scenario, result.record_id);
      console.log('Custom code response:', response);
      
      // Update the result with the new code
      if (response.data && response.data.code_data) {
        // Create a copy of the current result
        const updatedResult = JSON.parse(JSON.stringify(result));
        
        // Add the new code to the appropriate topic or create a new topic
        const codeData = response.data.code_data;
        
        // Use the formattedSubtopicData logic for consistency
        const customTopicKey = "Custom Codes (N/A)"; // Define a key for custom codes
        
        // Ensure CDT_subtopic exists
        if (!updatedResult.CDT_subtopic) {
          updatedResult.CDT_subtopic = [];
        }
        
        // Find or create the custom topic entry in the original array format
        let customTopicEntry = updatedResult.CDT_subtopic.find(t => t.topic === "Custom Codes");
        if (!customTopicEntry) {
          customTopicEntry = { topic: "Custom Codes", code_range: "N/A", codes: [] };
          updatedResult.CDT_subtopic.push(customTopicEntry);
        }
        
        // Extract applicability status from the response data directly
        const isApplicable = codeData.isApplicable;
        
        // Extract reason from the structured explanation
        let reason = "N/A";
        if (codeData.explanation) {
          const reasonMatch = codeData.explanation.match(/\*\*Reason\*\*:\s*([\s\S]*)/i);
          reason = reasonMatch ? reasonMatch[1].trim() : codeData.explanation; // Fallback to full explanation if pattern fails
        }
        
        // Add the new code data with parsed information
        customTopicEntry.codes.push({
          code: codeData.code,
          explanation: reason, // Use the extracted reason
          doubt: codeData.doubt || "None",
          isApplicable: isApplicable, // Store applicability directly
          raw_data: codeData.explanation // Store the original structured explanation as raw_data
        });
        
        // If there are inspector results, add the code there too if applicable
        if (updatedResult.inspector_results) {
          const inspectorData = updatedResult.inspector_results; // Direct access
          
          if (isApplicable && inspectorData.cdt) {
            // Ensure codes array exists
            if (!inspectorData.cdt.codes) inspectorData.cdt.codes = [];
            // Add to accepted codes if applicable and not already present
            if (!inspectorData.cdt.codes.includes(codeData.code)) {
              inspectorData.cdt.codes.push(codeData.code);
            }
            // Ensure rejected_codes array exists and remove if present
             if (!inspectorData.cdt.rejected_codes) inspectorData.cdt.rejected_codes = [];
             inspectorData.cdt.rejected_codes = inspectorData.cdt.rejected_codes.filter(c => c !== codeData.code);
          } else if (!isApplicable && inspectorData.cdt) {
             // Add to rejected codes if not applicable and not already present
             if (!inspectorData.cdt.rejected_codes) inspectorData.cdt.rejected_codes = [];
             if (!inspectorData.cdt.rejected_codes.includes(codeData.code)) {
                 inspectorData.cdt.rejected_codes.push(codeData.code);
             }
             // Ensure codes array exists and remove if present
             if (!inspectorData.cdt.codes) inspectorData.cdt.codes = [];
             inspectorData.cdt.codes = inspectorData.cdt.codes.filter(c => c !== codeData.code);
          }
        }
        
        // Update the result state
        setResult(updatedResult);
        
        // Expand the custom codes topic using the predefined key
         if (customTopicKey) { // Check if the key exists (it should)
              setExpandedTopics(prev => ({
                  ...prev,
                  [customTopicKey]: true // Use the variable here
              }));
          }
        
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
    <div className={`flex flex-col transition-colors`}>
      {/* Questioner Modal */}
      {result && (
        <Questioner
          isVisible={showQuestioner}
          onClose={handleQuestionerClose}
          questions={{
            cdt_questions: result.questioner_data?.cdt_questions?.questions || [],
            icd_questions: result.questioner_data?.icd_questions?.questions || []
          }}
          recordId={result.record_id || ''}
          onSubmitSuccess={handleQuestionerSuccess}
        />
      )}

      {/* Main content container */}
      <div className="flex-grow flex items-center justify-center p-4">
        <div className={`w-full p-4 md:p-6 ${isDark ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-lg transition-colors`}>
          {/* Header */}
          <div className={`${isDark ? 'bg-blue-900' : 'bg-blue-500'} text-white p-4 rounded-lg mb-6 transition-colors`}>
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
                  className={`block ${isDark ? 'text-gray-200' : 'text-gray-700'} font-medium mb-2 text-sm md:text-base`}
                >
                  Enter dental scenario to analyze:
                </label>
                <textarea
                  id="scenario"
                  name="scenario"
                  rows="6"
                  className={`w-full p-3 border ${
                    isDark ? 'bg-gray-700 border-gray-600 text-gray-100' : 'bg-white border-gray-300 text-gray-900'
                  } rounded-lg focus:outline-none ${
                    isDark ? 'focus:border-blue-400' : 'focus:border-blue-500'
                  } text-sm md:text-base transition-colors`}
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
                  className={`${
                    isDark ? 'bg-blue-700 hover:bg-blue-600' : 'bg-blue-600 hover:bg-blue-700'
                  } text-white px-4 py-2 md:px-6 md:py-2 rounded-lg shadow-md disabled:${
                    isDark ? 'bg-gray-700' : 'bg-gray-400'
                  } text-sm md:text-base transition-all duration-300 flex items-center justify-center`}
                  disabled={loading}
                >
                  {loading ? (
                    <>
                      <FaSpinner className="animate-spin mr-2" />
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <FaCogs className="inline mr-2" />
                      Analyze
                    </>
                  )}
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
                  <div className={`text-sm ${isDark ? 'text-gray-300' : 'text-gray-600'}`}>
                    Selected: {selectedCodes.accepted.length}
                  </div>
                </div>

                {/* Code Sections */}
                {formattedSubtopicData && Object.keys(formattedSubtopicData).length > 0 ? (
                  Object.keys(formattedSubtopicData).map((topicKey, index) => (
                    <div key={`topic-container-${index}-${topicKey}`}>{renderCodeSection(topicKey)}</div>
                  ))
                ) : (
                  <div className={`mt-4 p-4 ${isDark ? 'bg-gray-700' : 'bg-gray-50'} rounded-lg`}>
                    <p className={`${isDark ? 'text-gray-300' : 'text-gray-600'}`}>No subtopic code sections available for this analysis.</p>
                  </div>
                )}

                {/* Add Code Section */}
                <div className={`mt-6 p-4 ${isDark ? 'bg-gray-700 border-gray-600' : 'bg-gray-50 border-gray-200'} rounded-lg border`}>
                  <h3 className="text-lg font-semibold mb-3">Add Custom Code</h3>
                  <div className="flex items-center mb-2">
                    <input
                      type="text"
                      placeholder="Enter CDT code (e.g., D1120)"
                      className={`w-full p-2 border ${
                        isDark ? 'bg-gray-800 border-gray-600 text-gray-100' : 'bg-white border-gray-300 text-gray-900'
                      } rounded-lg focus:outline-none ${
                        isDark ? 'focus:border-blue-400' : 'focus:border-blue-500'
                      } text-sm md:text-base`}
                      value={newCode}
                      onChange={(e) => setNewCode(e.target.value)}
                      disabled={loading}
                    />
                    <button
                      onClick={handleAddCode}
                      className={`ml-2 px-4 py-2 ${
                        isDark ? 'bg-blue-700 hover:bg-blue-600' : 'bg-blue-600 hover:bg-blue-700'
                      } text-white rounded-lg shadow-md transition-all duration-300 disabled:${
                        isDark ? 'bg-gray-700' : 'bg-gray-400'
                      } flex items-center`}
                      disabled={loading || !newCode.trim() || !result?.record_id}
                    >
                      {loading ? 'Analyzing...' : 'Analyze Code'}
                    </button>
                  </div>
                  <p className={`text-xs ${isDark ? 'text-gray-400' : 'text-gray-500'} mt-1`}>
                    Add a custom CDT code to check if it&apos;s applicable to this scenario.
                    The AI will analyze and provide a recommendation.
                  </p>
                </div>

                {/* Submit Button */}
                <div className="mt-6 flex justify-end">
                  <button
                    onClick={handleSubmitCodes}
                    disabled={submitting || selectedCodes.accepted.length === 0}
                    className={`px-4 py-2 rounded-lg shadow-md flex items-center transition-all duration-300 text-white ${
                      selectedCodes.accepted.length > 0
                        ? (isDark ? 'bg-green-700 hover:bg-green-600' : 'bg-green-600 hover:bg-green-700')
                        : (isDark ? 'bg-gray-600' : 'bg-gray-400') + ' cursor-not-allowed'
                    } text-white`}
                  >
                    <FaPaperPlane className="mr-2" />
                    {submitting ? 'Submitting...' : `Submit ${selectedCodes.accepted.length} Accepted Code(s)`}
                  </button>
                </div>
              </div>
            )}

            {/* Error */}
            {error && (
              <div className={`mt-4 p-4 ${isDark ? 'bg-red-900/30' : 'bg-red-100'} rounded-lg`}>
                <h3 className={`font-semibold ${isDark ? 'text-red-300' : 'text-red-800'} text-sm md:text-base`}>Error:</h3>
                <p className={`text-xs md:text-sm ${isDark ? 'text-red-200' : 'text-red-700'}`}>{error}</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;