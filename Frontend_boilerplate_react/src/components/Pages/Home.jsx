import { FaCogs, FaCopy, FaSpinner, FaPlus } from 'react-icons/fa';
import { analyzeDentalScenario } from '../../interceptors/services.js';
import { useState, useEffect, useMemo } from 'react';
import Questioner from './Questioner.jsx';
import { useTheme } from '../../context/ThemeContext';
import Loader from '../Modal/Loading.jsx';

const Home = () => {
  useTheme();
  const [scenario, setScenario] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [selectedCodes, setSelectedCodes] = useState({ accepted: [], denied: [] });
  const [showQuestioner, setShowQuestioner] = useState(false);
  const [expandedTopics, setExpandedTopics] = useState({});
  const [newCode, setNewCode] = useState('');
  const [loadingProgress, setLoadingProgress] = useState(0);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);

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
      setExpandedTopics({});
      setNewCode('');
    };

    window.addEventListener('newAnalysis', resetForm);
    
    return () => {
      window.removeEventListener('newAnalysis', resetForm);
    };
  }, []);

  // Transform CDT_subtopic array into the object format needed by the component
  const formattedSubtopicData = useMemo(() => {
    if (!result?.CDT_subtopic) {
      return {};
    }
    
    console.log("Raw CDT_subtopic data:", result.CDT_subtopic);
    const formatted = {};
    
    result.CDT_subtopic.forEach(topic => {
      // Use a combination of topic name and code range as the key if possible
      const key = `${topic.topic || 'Unknown'} (${topic.code_range || 'N/A'})`;
      const allCodes = [];
      
      // First try to extract specific codes from subtopics_data
      if (topic.raw_result && topic.raw_result.subtopics_data && Array.isArray(topic.raw_result.subtopics_data)) {
        topic.raw_result.subtopics_data.forEach(subtopic => {
          // The raw_result can be an array or an object with raw_result property
          let rawResultsToProcess = [];
          
          if (Array.isArray(subtopic.raw_result)) {
            // Direct array of results
            rawResultsToProcess = subtopic.raw_result;
          } else if (typeof subtopic.raw_result === 'object' && subtopic.raw_result !== null) {
            // Get any specific entries that might contain codes
            rawResultsToProcess = [subtopic.raw_result];
          }
            
          rawResultsToProcess.forEach(codeEntry => {
            // Check if this is a direct entry with specific_codes
            if (codeEntry && Array.isArray(codeEntry.specific_codes) && codeEntry.specific_codes.length > 0) {
              codeEntry.specific_codes.forEach(code => {
                if (code) {
                  allCodes.push({
                    code: code,
                    explanation: codeEntry.explanation || 'No explanation provided',
                    doubt: codeEntry.doubt || 'None'
                  });
                }
              });
            }
          });
        });
      }
      
      // If we found specific codes, use them
      if (allCodes.length > 0) {
        console.log(`Found ${allCodes.length} specific codes for ${key}`);
        formatted[key] = allCodes;
      }
      // Fall back to the original codes array if present and no specific codes found
      else if (Array.isArray(topic.codes) && topic.codes.length > 0) {
        console.log(`Using fallback codes for ${key}: ${topic.codes.length} codes`);
        formatted[key] = topic.codes;
      }
    });
    
    console.log("Final formatted subtopic data:", formatted);
    return formatted;
  }, [result?.CDT_subtopic]);

  // Add a formatted ICD topic data state (after the formattedSubtopicData useMemo)
  const formattedICDTopicData = useMemo(() => {
    if (!result?.ICD_topic_result) {
      return null;
    }
    
    const icdTopicResult = result.ICD_topic_result;
    
    // Create a topic key similar to CDT topics format
    const categoryNumber = icdTopicResult.code_range || "N/A";
    const topicKey = `${icdTopicResult.topic || 'Unknown'} (${categoryNumber})`;
    
    // Format the ICD topic data to have a similar structure to CDT topics
    let formattedICDData = {};
    
    // Access data from raw_result if it exists, otherwise check direct properties
    const rawResult = icdTopicResult.raw_result || {};
    const code = rawResult.code || icdTopicResult.code;
    const explanation = rawResult.explanation || icdTopicResult.explanation || 'No explanation provided';
    const doubt = rawResult.doubt || icdTopicResult.doubt || 'None';
    const rawData = rawResult.raw_data || rawResult.raw_result || '';
    
    // Create a codes array with a single entry if the code exists
    if (code) {
      formattedICDData[topicKey] = [{
        code: code,
        explanation: explanation,
        doubt: doubt,
        raw_data: rawData
      }];
    } else {
      // Still create an entry for "No applicable code" but with clear indication
      formattedICDData[topicKey] = [{
        code: 'none', // explicitly set to 'none' to match topic service response
        explanation: explanation,
        doubt: doubt,
        raw_data: rawData
      }];
    }
    
    return formattedICDData;
  }, [result?.ICD_topic_result]);

  // Initialize expanded topics state based on the formatted data
  useEffect(() => {
    const initialExpandedState = {};
    
    // Handle CDT subtopics
    if (formattedSubtopicData && Object.keys(formattedSubtopicData).length > 0) {
      console.log("Formatted Subtopics data:", formattedSubtopicData);
      Object.keys(formattedSubtopicData).forEach(topicKey => {
        initialExpandedState[topicKey] = false;
      });
    }
    
    // Also handle ICD topic
    if (formattedICDTopicData && Object.keys(formattedICDTopicData).length > 0) {
      console.log("Formatted ICD Topic data:", formattedICDTopicData);
      Object.keys(formattedICDTopicData).forEach(topicKey => {
        initialExpandedState[topicKey] = false; // Default to collapsed
      });
    }
    
    if (Object.keys(initialExpandedState).length > 0) {
      setExpandedTopics(initialExpandedState);
    } else {
      setExpandedTopics({}); // Reset if no data
    }
  }, [formattedSubtopicData, formattedICDTopicData]); // Add dependency on ICD data

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
    } catch (err) {
      console.error('Error analyzing scenario:', err);
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

  const scrollToCode = (code) => {
    // Find the topic containing the code using formattedSubtopicData
    let foundTopicKey = null;
    let codeIndex = -1;
    
    console.log("Looking for code:", code);
    console.log("Available topics:", Object.keys(formattedSubtopicData));
    
    // Search through the formatted data
    if (formattedSubtopicData) {
      Object.keys(formattedSubtopicData).forEach(topicKey => {
        const topicCodes = formattedSubtopicData[topicKey];
        if (topicCodes && Array.isArray(topicCodes)) {
          topicCodes.forEach((codeData, index) => {
            // Check both direct code equality and specific_codes arrays
            const codeMatch = 
              (codeData && codeData.code === code) || 
              (codeData && Array.isArray(codeData.specific_codes) && codeData.specific_codes.includes(code));
              
            if (codeMatch) {
              console.log(`Found code ${code} in topic ${topicKey}`);
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
            element.classList.remove('bg-red-100');
          }, 1500);
        } else {
          console.log(`Could not find element with ID code-${code}`);
        }
      }, 300);
    } else {
      console.log(`Could not find topic containing code ${code}`);
    }
  };

  const handleAddCustomCode = async () => {
    if (!newCode.trim()) {
      return;
    }

    const codeType = document.getElementById('codeType').value; // Get the selected code type
    const codes = result?.inspector_results?.[codeType.toLowerCase()]?.codes || [];
    
    if (codes.includes(newCode)) {
      return;
    }

    try {
      // Update the inspector results with the new code
      const updatedResult = { ...result };
      updatedResult.inspector_results[codeType.toLowerCase()].codes.push(newCode);
      setResult(updatedResult);
      setNewCode('');
      
      // Automatically select the new code
      handleCodeSelection(newCode, 'accept');
    } catch (err) {
      // Handle potential errors, e.g., logging
      console.error("Error adding custom code:", err);
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
                  className="text-[var(--color-text-secondary)] hover:text-[var(--color-primary)] hover:scale-105 transition-all duration-200"
                >
                  <FaCopy />
                </button>
              </div>
              <div className="flex flex-wrap gap-2">
                {result?.inspector_results?.cdt?.codes.map((code, index) => (
                  <span
                    key={`${code}-${index}`}
                    onClick={() => handleCodeSelection(code, selectedCodes.accepted.includes(code) ? 'deny' : 'accept')}
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
                  className="text-[var(--color-text-secondary)] hover:text-[var(--color-primary)] hover:scale-105 transition-all duration-200"
                >
                  <FaCopy />
                </button>
              </div>
              <div className="flex flex-wrap gap-2">
                {result?.inspector_results?.icd?.codes.map((code, index) => (
                  <span
                    key={`icd-code-${index}-${code}`}
                    onClick={() => handleCodeSelection(code, selectedCodes.accepted.includes(code) ? 'deny' : 'accept')}
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
          <div className="border border-[var(--color-border)] bg-[var(--color-input-bg)] p-4 rounded-lg shadow-md font-bold leading-relaxed text-[var(--color-text-primary)]">
            &nbsp; {/* Placeholder content */}
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
                {result?.inspector_results?.cdt?.codes.map((code) => (
                  <tr key={code} className="border-t border-[var(--color-border)]">
                    <td className="p-2">{code}</td>
                    <td className="p-2">CDT</td>
                    <td className="p-2">{/* Add description from your data */}</td>
                    <td className="p-2">
                      <button className="text-[var(--color-primary)] hover:text-[var(--color-primary-hover)] font-medium" onClick={() => scrollToCode(code)}>
                        View
                      </button>
                      <button className="text-green-400 hover:text-green-500 ml-2 font-medium">
                        Add to Claim
                      </button>
                    </td>
                  </tr>
                ))}
                {result?.inspector_results?.icd?.codes.map((code) => (
                  <tr key={code} className="border-t border-[var(--color-border)]">
                    <td className="p-2">{code}</td>
                    <td className="p-2">ICD-10</td>
                    <td className="p-2">{/* Add description from your data */}</td>
                    <td className="p-2">
                      <button className="text-[var(--color-primary)] hover:text-[var(--color-primary-hover)] font-medium">View</button>
                      <button className="text-green-400 hover:text-green-500 ml-2 font-medium">
                        Add to Claim
                      </button>
                    </td>
                  </tr>
                ))}
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