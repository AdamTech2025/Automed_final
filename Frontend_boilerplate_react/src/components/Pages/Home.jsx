import { FaCogs, FaCopy, FaSpinner, FaPlus } from 'react-icons/fa';
import { analyzeDentalScenario, addCustomCode } from '../../interceptors/services.js';
import { useState, useEffect, useMemo } from 'react';
import Questioner from './Questioner.jsx';
import { useTheme } from '../../context/ThemeContext';
import Loader from '../Modal/Loading.jsx';
import { message } from 'antd';

// Helper function to escape regex special characters
const escapeRegex = (string) => {
  // Escape characters with special meaning in regex.
  // Handles cases like '.' in ICD codes (e.g., K08.89)
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); // $& means the whole matched string
}

const Home = () => {
  useTheme();
  const [scenario, setScenario] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [selectedCodes, setSelectedCodes] = useState({ accepted: [], denied: [] });
  const [showQuestioner, setShowQuestioner] = useState(false);
  const [newCode, setNewCode] = useState('');
  const [loadingProgress, setLoadingProgress] = useState(0);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [activeCodeDetail, setActiveCodeDetail] = useState(null);
  const [expandedHistoryRows, setExpandedHistoryRows] = useState({});

  // Check if there are questions in the result
  useEffect(() => {
    if (result && result.questioner_data && result.questioner_data.has_questions) {
      setShowQuestioner(true);
    } else {
      setShowQuestioner(false);
    }
  }, [result]);

  // Fake progress simulation
  useEffect(() => {
    let progressInterval;
    
    if (loading) {
      setLoadingProgress(0);
      const totalTime = 550000; // 5.5 minutes in milliseconds
      const intervalTime = 1000; // Update every second
      const increments = totalTime / intervalTime;
      const incrementAmount = 100 / increments;
      
      progressInterval = setInterval(() => {
        setLoadingProgress(prevProgress => {
          const newProgress = prevProgress + incrementAmount;
          // Cap at 95% so it doesn't look complete before the actual data arrives
          return newProgress >= 95 ? 95 : newProgress;
        });
      }, intervalTime);
    } else {
      // Reset progress when loading is complete
      setLoadingProgress(0);
    }
    
    return () => {
      if (progressInterval) clearInterval(progressInterval);
    };
  }, [loading]);

  // Listen for the newAnalysis event from Navbar
  useEffect(() => {
    const resetForm = (event) => {
      console.log("New analysis event received, resetting form", event.detail);
      setScenario('');
      setResult(null);
      setSelectedCodes({ accepted: [], denied: [] });
      setNewCode('');
      setActiveCodeDetail(null);
    };

    window.addEventListener('newAnalysis', resetForm);
    
    return () => {
      window.removeEventListener('newAnalysis', resetForm);
    };
  }, []);

  // Consolidate all code details into a map for easier lookup
  const allCodeDetailsMap = useMemo(() => {
    const detailsMap = {};
    if (!result) return detailsMap;

    // 1. Process CDT Topic Activation Results for detailed explanations
    if (result.cdt_topic_activation_results && Array.isArray(result.cdt_topic_activation_results)) {
      result.cdt_topic_activation_results.forEach(topic => {
        const topicName = topic.topic || 'Unknown Topic';
        if (topic.raw_result?.subtopics_data && Array.isArray(topic.raw_result.subtopics_data)) {
          topic.raw_result.subtopics_data.forEach(subtopic => {
            const subtopicName = subtopic.topic || 'Unknown Subtopic';
            // Check the new structure with parsed_result
            if (subtopic.parsed_result && Array.isArray(subtopic.parsed_result)) {
               subtopic.parsed_result.forEach(parsedEntry => {
                  if (parsedEntry?.specific_codes && Array.isArray(parsedEntry.specific_codes)) {
                     parsedEntry.specific_codes.forEach(code => {
                        if (code && !detailsMap[code]) { // Prioritize first explanation found
                           detailsMap[code] = {
                              code: code,
                              type: 'CDT',
                              explanation: parsedEntry.explanation || 'No explanation provided.',
                              doubt: parsedEntry.doubt || 'None',
                              topic: topicName,
                              subtopic: subtopicName
                           };
                        }
                     });
                  }
               });
            }
          });
        }
      });
    }

    // 2. Process ICD Topic Activation Result
    const icdTopic = result.icd_topic_activation_results;
    if (icdTopic?.raw_result?.code && icdTopic.raw_result.code !== 'none') {
       const code = icdTopic.raw_result.code;
       if (!detailsMap[code]) {
          detailsMap[code] = {
             code: code,
             type: 'ICD-10',
             explanation: icdTopic.raw_result.explanation || 'No explanation provided.',
             doubt: icdTopic.raw_result.doubt || 'None',
             topic: icdTopic.topic || 'ICD Topic',
             subtopic: null
          };
       }
    }

    // 3. Add info for codes from Inspector results if not already mapped
    const inspectorCdtCodes = result.inspector_results?.cdt?.codes || [];
    const inspectorIcdCodes = result.inspector_results?.icd?.codes || [];
    const inspectorCdtExplanation = result.inspector_results?.cdt?.explanation || '';
    const inspectorIcdExplanation = result.inspector_results?.icd?.explanation || '';

    // Function to extract explanation for a specific code from the inspector string
    const getInspectorExplanation = (code, explanationString) => {
      // Escape the code before inserting into regex
      const escapedCode = escapeRegex(code);
      // Simplified regex: Require exactly two asterisks **CODE(...)**: Selected.
      const regex = new RegExp(`- \*\*${escapedCode}\s*\([^)]*\)\*\*:\s*Selected\.\s*(.*?)(?=\s*-\s*\*\*|$)`, 'i');
      const match = explanationString.match(regex);
      // console.log(`Regex for ${code}:`, regex, `Match:`, match); // Debugging log
      return match ? match[1].trim() : 'Explanation from final inspection result.'; // Fallback explanation
    };

    inspectorCdtCodes.forEach(code => {
      if (code && !detailsMap[code]) {
        detailsMap[code] = {
          code: code,
          type: 'CDT',
          explanation: getInspectorExplanation(code, inspectorCdtExplanation),
          doubt: 'N/A',
          topic: 'Final Selection (Inspector)',
          subtopic: null
        };
      }
    });

    inspectorIcdCodes.forEach(code => {
      if (code && !detailsMap[code]) {
        detailsMap[code] = {
          code: code,
          type: 'ICD-10',
          // ICD inspector explanation might be general, not per-code
          explanation: inspectorIcdExplanation || 'Explanation from final inspection result.',
          doubt: 'N/A',
          topic: 'Final Selection (Inspector)',
          subtopic: null
        };
      }
    });

    // 4. Add rejected codes from inspector if not present
    const rejectedCdt = result.inspector_results?.cdt?.rejected_codes || [];
    const rejectedIcd = result.inspector_results?.icd?.rejected_codes || [];

     rejectedCdt.forEach(code => {
       if (code && !detailsMap[code]) {
         detailsMap[code] = {
           code: code,
           type: 'CDT',
           explanation: 'Code was suggested but rejected during final inspection.',
           doubt: 'N/A',
           topic: 'Rejected Suggestion',
           subtopic: null
         };
       }
     });
     rejectedIcd.forEach(code => {
       if (code && !detailsMap[code]) {
         detailsMap[code] = {
           code: code,
           type: 'ICD-10',
           explanation: 'Code was suggested but rejected during final inspection.',
           doubt: 'N/A',
           topic: 'Rejected Suggestion',
           subtopic: null
         };
       }
     });


    console.log("Generated allCodeDetailsMap:", detailsMap);
    return detailsMap;
  }, [result]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    setSelectedCodes({ accepted: [], denied: [] });

    try {
      const response = await analyzeDentalScenario({ scenario });
      console.log('Analysis results received:', response);
      console.log('Record ID:', response?.record_id);
      setResult(response);
      message.success('Analysis complete!');
    } catch (err) {
      console.error('Error analyzing scenario:', err);
      message.error('Analysis failed. Please try again.');
    } finally {
      setLoading(false);
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
      // const errorMsg = Array.isArray(response) // Removed unused errorMsg assignment
      //   ? response.find(r => r.response && r.response.status === 'error')?.response?.message || 'An error occurred in batch processing.'
      //   : response?.message || 'Failed to process answers';
      // Don't hide the questioner modal on error
    }
  };


  const handleAddCustomCode = async () => {
    if (!newCode.trim()) {
      message.warning("Please enter a code.");
      return;
    }

    const codeType = document.getElementById('codeType').value;

    // Check if code already exists (client-side check before API call)
    if (selectedCodes.accepted.includes(newCode) || selectedCodes.denied.includes(newCode)) {
       message.warning(`${newCode} has already been processed.`);
       setNewCode('');
       return;
    }

    // Call the API to add the custom code
    setLoading(true);
    try {
      const response = await addCustomCode(newCode, scenario, result?.record_id);
      console.log("Add Custom Code API response:", response);

      // OPTIONAL: Update UI based on response.data if backend returns updated state
      // For now, just add it client-side assuming success
      if (response.status === 'success') {
        setSelectedCodes(prev => ({
          ...prev,
          accepted: [...prev.accepted, newCode]
        }));
        // Update details map (assuming backend doesn't return full updated map)
        const customDetail = {
          code: newCode,
          type: codeType,
          explanation: response.data?.code_data?.explanation || 'Manually added custom code.',
          doubt: response.data?.code_data?.doubt || 'N/A',
          topic: 'Custom',
          subtopic: null
        };
        // This won't update the map derived from useMemo directly.
        // A more robust solution might involve triggering a re-fetch or merging the response.

        handleShowCodeDetail(newCode);
        message.success(response.message || `Added custom code: ${newCode}`);
        setNewCode('');
      } else {
         message.error(response.message || 'Failed to add custom code via API.');
      }
    } catch (apiError) {
      console.error("Error calling addCustomCode API:", apiError);
      message.error(apiError.message || 'An error occurred while adding the custom code.');
    } finally {
        setLoading(false);
    }
  };

  const handleFileUpload = (file) => {
    setUploadedFile(file);
    let progress = 0;
    const interval = setInterval(() => {
      progress += 10;
      setUploadProgress(progress);
      if (progress >= 100) {
        clearInterval(interval);
        setUploadProgress(0);
        handleSubmit(new Event('submit')); // Simulate form submission
      }
    }, 200);
  };

  return (
    <div className="flex-1 p-4 md:p-8 bg-[var(--color-bg-primary)] text-[var(--color-text-primary)]">
      {/* Main Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Input Section */}
        <div className="bg-[var(--color-bg-secondary)] p-6 rounded-xl shadow-lg col-span-1 md:col-span-2">
          <h3 className="text-lg font-bold tracking-tight mb-4 text-[var(--color-text-primary)]">Input Clinical Notes</h3>
          <div className="mb-4">
            <label className="block text-[var(--color-text-secondary)] mb-2 text-sm font-medium">Raw Text Input</label>
            <textarea
              value={scenario}
              onChange={(e) => setScenario(e.target.value)}
              className="w-full border rounded-lg p-3 bg-[var(--color-input-bg)] text-[var(--color-text-primary)] border-[var(--color-border)] focus:ring-2 focus:ring-[var(--color-primary)] text-sm font-light leading-relaxed"
              rows="5"
              placeholder="Enter clinical notes (e.g., Patient has tooth decay in molar, requires filling)"
            />
          </div>
          <div className="mb-4">
            <label className="block text-[var(--color-text-secondary)] mb-2 text-sm font-medium">Upload PDF</label>
            <div 
              className="border-2 border-dashed border-[var(--color-border)] p-6 rounded-lg text-center hover:border-[var(--color-primary)] transition-colors"
              onDragOver={(e) => e.preventDefault()}
              onDrop={(e) => {
                e.preventDefault();
                const file = e.dataTransfer.files[0];
                if (file && file.type === 'application/pdf') {
                  handleFileUpload(file);
                }
              }}
            >
              <input
                type="file"
                accept=".pdf"
                className="hidden"
                onChange={(e) => {
                  const file = e.target.files?.[0];
                  if (file) handleFileUpload(file);
                }}
              />
              <p className="text-[var(--color-text-secondary)] text-sm font-light leading-relaxed">
                Drag and drop a PDF or <span className="text-[var(--color-primary)] cursor-pointer hover:underline">browse</span>
              </p>
              {uploadedFile && (
                <p className="text-[var(--color-text-secondary)] mt-2 text-sm font-light">
                  {uploadedFile.name}
                </p>
              )}
              {uploadProgress > 0 && uploadProgress < 100 && (
                <div className="w-full bg-[var(--color-border)] rounded-full h-2 mt-2">
                  <div
                    className="bg-[var(--color-primary)] h-2 rounded-full"
                    style={{ width: `${uploadProgress}%` }}
                  />
                </div>
              )}
            </div>
          </div>
          <button
            onClick={handleSubmit}
            disabled={loading}
            className="bg-[var(--color-primary)] hover:bg-[var(--color-primary-hover)] text-white px-4 py-2 text-sm rounded-lg hover:scale-105 hover:shadow-lg focus:ring-2 focus:ring-[var(--color-primary)] font-medium transition-all duration-200"
          >
            {loading ? (
              <>
                <FaSpinner className="animate-spin inline mr-2" />
                Processing...
              </>
            ) : (
              <>
                <FaCogs className="inline mr-2" />
                Process Input
              </>
            )}
          </button>
        </div>

        {/* Final Codes Section - Add space-y-6 for better vertical spacing */}
        <div className="bg-[var(--color-bg-secondary)] p-6 rounded-xl shadow-lg hover:shadow-xl transition-all duration-200 space-y-6">
          {/* Header: Title and Copy Button */}
          <div className="flex justify-between items-center">
            <h3 className="text-lg font-bold tracking-tight text-[var(--color-text-primary)]">Final Codes</h3>
            <button
              className="bg-[var(--color-primary)] hover:bg-[var(--color-primary-hover)] text-white px-3 py-1 text-sm rounded-lg hover:scale-105 hover:shadow-lg focus:ring-2 focus:ring-[var(--color-primary)] flex items-center font-medium"
            >
              <FaCopy className="mr-2" /> Copy Selected
            </button>
          </div>

          {/* Custom Code Input Form */}
          <div className="mb-4">
            <h4 className="text-sm font-semibold text-[var(--color-text-secondary)] mb-2">Add Custom Code</h4>
            <div className="flex flex-col sm:flex-row flex-wrap gap-2">
              <input
                type="text"
                value={newCode}
                onChange={(e) => setNewCode(e.target.value)}
                className="flex-1 border rounded-lg p-2 text-sm bg-[var(--color-input-bg)] text-[var(--color-text-primary)] border-[var(--color-border)] focus:ring-2 focus:ring-[var(--color-primary)] font-light leading-relaxed"
                placeholder="Enter code (e.g., D0120)"
              />
              <select
                id="codeType"
                className="border rounded-lg p-2 text-sm bg-[var(--color-input-bg)] text-[var(--color-text-primary)] border-[var(--color-border)] focus:ring-2 focus:ring-[var(--color-primary)] font-light leading-relaxed"
              >
                <option value="CDT">CDT</option>
                <option value="ICD">ICD-10</option>
              </select>
              <button
                onClick={handleAddCustomCode}
                className="bg-[var(--color-primary)] hover:bg-[var(--color-primary-hover)] text-white px-3 py-1 text-sm rounded-lg hover:scale-105 hover:shadow-lg focus:ring-2 focus:ring-[var(--color-primary)] font-medium"
              >
                Add
              </button>
            </div>
          </div>

          {/* Code Output */}
          <div className="space-y-4">
            {/* CDT Codes */}
            <div className="border border-[var(--color-border)] bg-[var(--color-input-bg)] p-4 rounded-lg shadow-md">
              <div className="flex justify-between items-center mb-2">
                <h4 className="text-lg font-semibold text-[var(--color-text-primary)]">CDT Codes</h4>
                <button
                  onClick={() => {
                    const acceptedCdtCodes = (result?.inspector_results?.cdt?.codes || []).filter(code => selectedCodes.accepted.includes(code));
                    if (acceptedCdtCodes.length === 0) {
                      message.warning('No accepted CDT codes to copy.');
                      return;
                    }
                    const textToCopy = acceptedCdtCodes.join(', ');
                    navigator.clipboard.writeText(textToCopy)
                      .then(() => message.success(`Copied CDT: ${textToCopy}`))
                      .catch(() => message.error('Failed to copy CDT codes.'));
                  }}
                  disabled={!(result?.inspector_results?.cdt?.codes || []).some(code => selectedCodes.accepted.includes(code))}
                  className="text-[var(--color-text-secondary)] hover:text-[var(--color-primary)] hover:scale-105 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed p-1"
                  aria-label="Copy Accepted CDT Codes"
                >
                  <FaCopy />
                </button>
              </div>
              <div className="flex flex-wrap gap-2">
                {result?.inspector_results?.cdt?.codes.map((code, index) => (
                  <span
                    key={`${code}-${index}`}
                    onClick={() => {
                      handleCodeSelection(code, selectedCodes.accepted.includes(code) ? 'deny' : 'accept');
                      setActiveCodeDetail(code);
                    }}
                    className={`cursor-pointer px-2 py-1 rounded-full text-xs transition-all duration-200 hover:scale-105 hover:shadow-lg border
                      ${
                        selectedCodes.accepted.includes(code)
                          ? 'bg-green-100 dark:bg-green-900/60 text-green-900 dark:text-green-200 border-green-300 dark:border-green-700'
                          : selectedCodes.denied.includes(code)
                          ? 'bg-red-100 dark:bg-red-900/60 text-red-900 dark:text-red-200 border-red-300 dark:border-red-700'
                          : 'bg-[var(--color-input-bg)] text-[var(--color-text-secondary)] border-[var(--color-border)]'
                      }`}
                  >
                    {code}
                  </span>
                ))}
              </div>
            </div>

            {/* ICD Codes */}
            <div className="border border-[var(--color-border)] bg-[var(--color-input-bg)] p-4 rounded-lg shadow-md">
              <div className="flex justify-between items-center mb-2">
                <h4 className="text-lg font-semibold text-[var(--color-text-primary)]">ICD-10 Codes</h4>
                <button
                  onClick={() => {
                    const acceptedIcdCodes = (result?.inspector_results?.icd?.codes || []).filter(code => selectedCodes.accepted.includes(code));
                    if (acceptedIcdCodes.length === 0) {
                      message.warning('No accepted ICD-10 codes to copy.');
                      return;
                    }
                    const textToCopy = acceptedIcdCodes.join(', ');
                    navigator.clipboard.writeText(textToCopy)
                      .then(() => message.success(`Copied ICD-10: ${textToCopy}`))
                      .catch(() => message.error('Failed to copy ICD-10 codes.'));
                  }}
                  disabled={!(result?.inspector_results?.icd?.codes || []).some(code => selectedCodes.accepted.includes(code))}
                  className="text-[var(--color-text-secondary)] hover:text-[var(--color-primary)] hover:scale-105 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed p-1"
                  aria-label="Copy Accepted ICD-10 Codes"
                >
                  <FaCopy />
                </button>
              </div>
              <div className="flex flex-wrap gap-2">
                {result?.inspector_results?.icd?.codes.map((code, index) => (
                  <span
                    key={`icd-code-${index}-${code}`}
                    onClick={() => {
                      handleCodeSelection(code, selectedCodes.accepted.includes(code) ? 'deny' : 'accept');
                      setActiveCodeDetail(code);
                    }}
                    className={`cursor-pointer px-2 py-1 rounded-full text-xs transition-all duration-200 hover:scale-105 hover:shadow-lg border
                      ${
                        selectedCodes.accepted.includes(code)
                          ? 'bg-green-100 dark:bg-green-900/60 text-green-900 dark:text-green-200 border-green-300 dark:border-green-700'
                          : selectedCodes.denied.includes(code)
                          ? 'bg-red-100 dark:bg-red-900/60 text-red-900 dark:text-red-200 border-red-300 dark:border-red-700'
                          : 'bg-[var(--color-input-bg)] text-[var(--color-text-secondary)] border-[var(--color-border)]'
                      }`}
                  >
                    {code}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Code Details Section */}
        <div className="bg-[var(--color-bg-secondary)] p-6 rounded-xl shadow-lg hover:shadow-xl transition-all duration-200 col-span-1 md:col-span-3">
          <h3 className="text-lg font-bold tracking-tight mb-4 text-[var(--color-text-primary)]">Code Details</h3>
          <div className="border border-[var(--color-border)] bg-[var(--color-input-bg)] p-4 rounded-lg shadow-inner min-h-[100px] text-sm font-light leading-relaxed text-[var(--color-text-primary)]">
            {activeCodeDetail && allCodeDetailsMap[activeCodeDetail] ? (
              <div className="space-y-2">
                <p><strong className="font-medium text-[var(--color-text-secondary)]">Code:</strong> {allCodeDetailsMap[activeCodeDetail].code}</p>
                <p><strong className="font-medium text-[var(--color-text-secondary)]">Type:</strong> {allCodeDetailsMap[activeCodeDetail].type}</p>
                <p><strong className="font-medium text-[var(--color-text-secondary)]">Explanation:</strong> {allCodeDetailsMap[activeCodeDetail].explanation}</p>
              </div>
            ) : (
              <p className="text-[var(--color-text-secondary)]">Click a code in the &apos;Verify Codes&apos; section or &apos;View Details&apos; in the summary table to see details here.</p>
            )}
          </div>
        </div>

        {/* Recent Codes Dashboard */}
        <div className="bg-[var(--color-bg-secondary)] p-6 rounded-xl shadow-lg col-span-1 md:col-span-3">
          <h3 className="text-lg font-bold tracking-tight mb-4 text-[var(--color-text-primary)]">Final Code Generation History</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="text-[var(--color-text-secondary)] font-medium">
                  <th className="p-2">Code</th>
                  <th className="p-2">Type</th>
                  <th className="p-2">Description</th>
                  <th className="p-2">Actions</th>
                </tr>
              </thead>
              <tbody className="font-bold text-[var(--color-text-primary)] leading-relaxed">
                {result?.inspector_results?.cdt?.codes.map((code, index) => {
                  const details = allCodeDetailsMap[code] || { description: 'Details not found.' };
                  const rowKey = `history-${code}-${index}`;
                  const isExpanded = expandedHistoryRows[rowKey] || false;
                  const explanation = details.explanation || 'N/A';
                  const needsReadMore = explanation.length > 100;
                  return (
                    <tr key={`history-${code}-${index}`} className="hover:bg-[var(--color-bg-primary)] transition-colors duration-150">
                      <td className="p-2 font-medium">{code}</td>
                      <td className="p-2">{details.type}</td>
                      <td className="p-2 text-xs font-light max-w-md">
                        {needsReadMore && !isExpanded ? (
                          <>
                            {explanation.substring(0, 100)}...
                            <button
                              onClick={() => setExpandedHistoryRows(prev => ({ ...prev, [rowKey]: true }))}
                              className="text-blue-500 dark:text-blue-400 hover:underline ml-1 text-xs"
                            >
                              Read More
                            </button>
                          </>
                        ) : (
                          <>
                            {explanation}
                            {needsReadMore && isExpanded && (
                              <button
                                onClick={() => setExpandedHistoryRows(prev => ({ ...prev, [rowKey]: false }))}
                                className="text-blue-500 dark:text-blue-400 hover:underline ml-1 text-xs"
                              >
                                Read Less
                              </button>
                            )}
                          </>
                        )}
                      </td>
                      <td className="p-2">
                        <button
                          className="text-[var(--color-primary)] hover:text-[var(--color-primary-hover)] hover:underline font-medium text-xs"
                          onClick={() => setActiveCodeDetail(code)}
                        >
                          View Details
                        </button>
                      </td>
                    </tr>
                  );
                })}
                {result?.inspector_results?.icd?.codes.map((code, index) => {
                  const details = allCodeDetailsMap[code] || { description: 'Details not found.' };
                  const rowKey = `history-${code}-${index}`;
                  const isExpanded = expandedHistoryRows[rowKey] || false;
                  const explanation = details.explanation || 'N/A';
                  const needsReadMore = explanation.length > 100;
                  return (
                    <tr key={`history-${code}-${index}`} className="hover:bg-[var(--color-bg-primary)] transition-colors duration-150">
                      <td className="p-2 font-medium">{code}</td>
                      <td className="p-2">{details.type}</td>
                      <td className="p-2 text-xs font-light max-w-md">
                        {needsReadMore && !isExpanded ? (
                          <>
                            {explanation.substring(0, 100)}...
                            <button
                              onClick={() => setExpandedHistoryRows(prev => ({ ...prev, [rowKey]: true }))}
                              className="text-blue-500 dark:text-blue-400 hover:underline ml-1 text-xs"
                            >
                              Read More
                            </button>
                          </>
                        ) : (
                          <>
                            {explanation}
                            {needsReadMore && isExpanded && (
                              <button
                                onClick={() => setExpandedHistoryRows(prev => ({ ...prev, [rowKey]: false }))}
                                className="text-blue-500 dark:text-blue-400 hover:underline ml-1 text-xs"
                              >
                                Read Less
                              </button>
                            )}
                          </>
                        )}
                      </td>
                      <td className="p-2">
                        <button
                          className="text-[var(--color-primary)] hover:text-[var(--color-primary-hover)] hover:underline font-medium text-xs"
                          onClick={() => setActiveCodeDetail(code)}
                        >
                          View Details
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      </div>

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

      {/* Loading Overlay */}
      {loading && (
        <div className="fixed inset-0 bg-black bg-opacity-70 flex flex-col items-center justify-center z-50 backdrop-blur-md">
          <div className="bg-gradient-to-b from-blue-900 to-gray-900 p-10 rounded-xl shadow-2xl max-w-lg w-full mx-4">
            <div className="flex justify-center">
              <div className="w-24 h-24">
                <Loader />
              </div>
            </div>
            <h3 className="text-white text-2xl font-bold mt-6 text-center">Analyzing your scenario...</h3>
            <div className="w-full bg-blue-800/30 h-2 my-4 rounded-full overflow-hidden">
              <div
                className="bg-gradient-to-r from-blue-500 to-blue-300 h-full rounded-full transition-all duration-1000 ease-linear"
                style={{ width: `${loadingProgress}%` }}
              />
            </div>
            <p className="text-blue-100 mt-3 text-center text-sm">({Math.round(loadingProgress)}% complete)</p>
            <p className="text-blue-100 mt-4 text-center">
              Our AI typically takes about 5 minutes to think. While you wait, you can start a new analysis in a separate tab.
            </p>
            <div className="flex justify-center mt-6">
              <button
                onClick={() => window.open(window.location.href, '_blank')}
                className="flex items-center px-4 py-2 bg-blue-700 hover:bg-blue-600 text-white rounded-md transition-colors"
              >
                <FaPlus className="mr-2" />
                New Analysis in New Tab
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Home;